#!/usr/bin/env python3
"""
gen_images.py — Generate images from script/image-prompts.md using AA accounts.

Strategy: **greedy fill** (not round-robin).
  - Fetch live balances for all valid AA accounts.
  - Sort accounts ascending by balance (drain smallest first).
  - Assign exactly floor(balance / COST_PER_PROMPT) prompts per account.
  - Execute concurrently across accounts, sequentially within each account.
  - If an account hits an error mid-batch, the failed prompts are reported at the end.

Usage:
    python gen_images.py --project <path>             # generate all missing images
    python gen_images.py --project <path> --dry-run   # show plan without generating
    python gen_images.py --project <path> --img IMG-02-01  # single image

Examples:
    python gen_images.py --project d:/business/content-vault/videos/boring-history/ming-grain-storage-1450
    python gen_images.py --project . --dry-run
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

import httpx
import yaml

log = logging.getLogger("gen_images")


# ── Config ────────────────────────────────────────────────────────────────────

def _find_config() -> Optional[Path]:
    here = Path(__file__).resolve().parent
    for candidate in [
        here.parent / "config" / "gen_images.yaml",
        here / "config" / "gen_images.yaml",
    ]:
        if candidate.exists():
            return candidate
    return None


def _load_config(path: Optional[Path] = None) -> dict:
    p = path or _find_config()
    if p and p.exists():
        with open(p, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}


_CFG = _load_config()

BASE_URL              = _CFG.get("api", {}).get("base_url", "http://localhost:8709")
MODEL_ID              = _CFG.get("generation", {}).get("model_id", "c3f4bea0-4cbf-49ea-b8ea-0b9d917ebc0c")
GENERATIONS_PER_MODEL = _CFG.get("generation", {}).get("generations_per_model", 2)
WIDTH                 = _CFG.get("generation", {}).get("width", 1920)
HEIGHT                = _CFG.get("generation", {}).get("height", 1080)
COST_PER_GEN          = _CFG.get("generation", {}).get("cost_per_gen", 0.144)
POLL_INTERVAL         = _CFG.get("generation", {}).get("poll_interval_secs", 3.0)
POLL_TIMEOUT          = _CFG.get("generation", {}).get("poll_timeout_secs", 300.0)

COST_PER_PROMPT = COST_PER_GEN * GENERATIONS_PER_MODEL  # 0.144 * 2 = 0.288


# ── Data types ────────────────────────────────────────────────────────────────

@dataclass
class PromptTask:
    img_id: str
    prompt: str


@dataclass
class AccountAlloc:
    email: str
    balance: float
    capacity: int
    tasks: list[PromptTask] = field(default_factory=list)


# ── Parsing ───────────────────────────────────────────────────────────────────

def _parse_header_meta(content: str) -> dict[str, str]:
    """Extract <!-- key: value --> metadata from the header comment block."""
    meta = {}
    for m in re.finditer(r"<!--\s*(style-suffix|title-suffix):\s*(.+?)\s*-->", content):
        meta[m.group(1)] = m.group(2).strip()
    return meta


def _parse_title_ids(content: str) -> set[str]:
    """Extract IMG IDs marked with [TITLE] in the prompt line."""
    ids: set[str] = set()
    # Match both formats: `IMG-XX-YY [TITLE]: ...` and code-block with [TITLE]
    for m in re.finditer(r"(IMG-\d{2}-\d{2})\s*\[TITLE\]", content):
        ids.add(m.group(1))
    return ids


def parse_image_prompts(script_dir: Path) -> list[PromptTask]:
    """
    Parse script/image-prompts.md.

    Supports header metadata for automatic suffix appending:
      <!-- style-suffix: classical oil painting style, 16:9 -->
      <!-- title-suffix: bold serif title bottom center: gold #D4A017 "TEXT", drop shadow -->

    Prompts marked with [TITLE] get both style-suffix AND title-suffix appended.
    Other prompts get only style-suffix appended.
    """
    prompts_file = script_dir / "image-prompts.md"
    if not prompts_file.exists():
        raise FileNotFoundError(f"image-prompts.md not found in {script_dir}")

    content = prompts_file.read_text(encoding="utf-8")
    meta = _parse_header_meta(content)
    title_ids = _parse_title_ids(content)

    style_suffix = meta.get("style-suffix", "")
    title_suffix = meta.get("title-suffix", "")

    # Support TWO formats:
    # Format A: IMG-XX-YY: <prompt text on one line>
    # Format B: ### IMG-XX-YY ... ```\n<prompt>\n```
    raw: list[tuple[str, str]] = []  # (img_id, prompt_text)

    for m in re.finditer(r"^(IMG-\d{2}-\d{2})(?:\s*\[TITLE\])?:\s*(.+)$", content, re.MULTILINE):
        raw.append((m.group(1), m.group(2).strip()))

    for m in re.finditer(
        r"^### (IMG-\d{2}-\d{2})(?:\s*\[TITLE\])?\b.*?\n```\n(.*?)\n```",
        content,
        re.MULTILINE | re.DOTALL,
    ):
        raw.append((m.group(1), " ".join(m.group(2).split())))

    if not raw:
        raise ValueError("No IMG-XX-XX prompts found in image-prompts.md")

    tasks = []
    for img_id, prompt_text in raw:
        # Build final prompt: scene + style suffix + optional title suffix
        parts = [prompt_text]
        if style_suffix:
            parts.append(style_suffix)
        if img_id in title_ids and title_suffix:
            parts.append(title_suffix)
        final = ", ".join(parts)
        tasks.append(PromptTask(img_id=img_id, prompt=final))

    return tasks


def find_missing_tasks(tasks: list[PromptTask], out_dir: Path) -> list[PromptTask]:
    """Return tasks where NOT ALL expected output images exist."""
    return [
        task for task in tasks
        if not all(
            (out_dir / f"{task.img_id}_{i}.png").exists()
            for i in range(1, GENERATIONS_PER_MODEL + 1)
        )
    ]


# ── API helpers ───────────────────────────────────────────────────────────────

async def _get_json(client: httpx.AsyncClient, url: str, **params) -> dict:
    r = await client.get(url, params=params, timeout=30)
    r.raise_for_status()
    body = r.json()
    if not body.get("success", True):
        raise RuntimeError(f"API error: {body.get('error', body)}")
    return body.get("data", body)


async def _post_json(client: httpx.AsyncClient, url: str, payload: dict) -> dict:
    r = await client.post(url, json=payload, timeout=60)
    r.raise_for_status()
    body = r.json()
    if not body.get("success", True):
        raise RuntimeError(f"API error: {body.get('error', body)}")
    return body.get("data", body)


async def fetch_valid_accounts(client: httpx.AsyncClient) -> list[dict]:
    """GET /accounts?service=ARTIFICIALANALYSIS → filter valid + not disabled."""
    data = await _get_json(client, f"{BASE_URL}/api/v1/accounts", service="ARTIFICIALANALYSIS")
    # data is a list of account dicts
    accounts: list[dict] = data if isinstance(data, list) else data.get("items", [])
    return [
        a for a in accounts
        if not a.get("disabled") and a.get("check_status") == "valid"
    ]


async def fetch_balance(
    client: httpx.AsyncClient,
    email: str,
    sem: asyncio.Semaphore,
) -> float:
    """GET /aa/session?email=... → org.balance as float.
    Raises if account hasn't accepted AA Terms of Use (can't generate images).
    """
    async with sem:
        data = await _get_json(client, f"{BASE_URL}/api/v1/aa/session", email=email)
    terms_accepted = data.get("user", {}).get("termsOfUseAcceptedAt")
    if terms_accepted is None:
        raise RuntimeError(f"Terms of Use not accepted — account cannot generate images")
    raw = data.get("org", {}).get("balance")
    if raw is None:
        raise RuntimeError(f"No balance in session response for {email}")
    return float(raw)


# ── Greedy fill ───────────────────────────────────────────────────────────────

def greedy_fill(
    tasks: list[PromptTask],
    balances: dict[str, float],
) -> tuple[list[AccountAlloc], list[PromptTask]]:
    """
    Distribute tasks across accounts using greedy fill.

    Sort accounts ASCENDING by balance (drain smallest first → more accounts fully utilized).
    Each account receives exactly floor(balance / COST_PER_PROMPT) tasks.

    Returns:
        allocs    — list of AccountAlloc (only accounts with at least 1 task assigned)
        remaining — tasks that could not be assigned (total credit exhausted)
    """
    eligible = [
        (email, bal)
        for email, bal in balances.items()
        if bal >= COST_PER_PROMPT
    ]
    eligible.sort(key=lambda x: x[1])  # ascending: drain smallest first

    allocs: list[AccountAlloc] = []
    remaining = list(tasks)

    for email, balance in eligible:
        if not remaining:
            break
        cap = int(balance / COST_PER_PROMPT)
        if cap <= 0:
            continue
        batch = remaining[:cap]
        remaining = remaining[cap:]
        allocs.append(AccountAlloc(
            email=email,
            balance=balance,
            capacity=cap,
            tasks=batch,
        ))

    return allocs, remaining


# ── Generation + download ─────────────────────────────────────────────────────

async def _generate(client: httpx.AsyncClient, email: str, task: PromptTask) -> str:
    """POST /aa/generate → generationId string."""
    data = await _post_json(client, f"{BASE_URL}/api/v1/aa/generate", {
        "email": email,
        "prompt": task.prompt,
        "model_ids": [MODEL_ID],
        "generations_per_model": GENERATIONS_PER_MODEL,
        "width": WIDTH,
        "height": HEIGHT,
    })
    gen_id = data.get("generationId") or data.get("id")
    if not gen_id:
        raise RuntimeError(f"No generationId in response for {task.img_id}: {data}")
    return gen_id


async def _poll_until_done(client: httpx.AsyncClient, email: str, gen_id: str) -> list[dict]:
    """
    Poll GET /aa/generation/{gen_id}?email=... every POLL_INTERVAL seconds.
    Raises TimeoutError if POLL_TIMEOUT exceeded.
    Returns list of AAImage dicts once all images are non-pending.
    """
    deadline = asyncio.get_event_loop().time() + POLL_TIMEOUT
    while True:
        if asyncio.get_event_loop().time() > deadline:
            raise TimeoutError(f"Generation {gen_id} timed out after {POLL_TIMEOUT}s")

        data = await _get_json(
            client,
            f"{BASE_URL}/api/v1/aa/generation/{gen_id}",
            email=email,
        )
        images: list[dict] = data.get("images", [])

        if images and all(img.get("status") != "pending" for img in images):
            return images

        await asyncio.sleep(POLL_INTERVAL)


async def _download_image(
    client: httpx.AsyncClient,
    email: str,
    image_id: str,
    filename_hint: str,
    out_path: Path,
) -> None:
    """POST /aa/image-download → PNG bytes → write to out_path."""
    r = await client.post(
        f"{BASE_URL}/api/v1/aa/image-download",
        json={"email": email, "image_id": image_id, "filename_hint": filename_hint},
        timeout=60,
    )
    r.raise_for_status()
    out_path.write_bytes(r.content)


# ── Per-account worker ────────────────────────────────────────────────────────

async def process_account(
    alloc: AccountAlloc,
    out_dir: Path,
    print_lock: asyncio.Lock,
    total_tasks: int,
    counter: list[int],  # shared mutable counter, mutated under print_lock
) -> list[tuple[str, str]]:
    """
    Process all tasks for one account fully concurrently.
    Fire all generations at once → poll all concurrently → download all concurrently.
    Returns list of (img_id, error_message) for any failures.
    """
    errors: list[tuple[str, str]] = []

    async with httpx.AsyncClient() as client:

        async def handle_task(task: PromptTask) -> None:
            gen_id = await _generate(client, alloc.email, task)

            async with print_lock:
                print(f"  [~/{total_tasks}] {task.img_id} @{alloc.email.split('@')[0]}  gen={gen_id[:8]}... polling")

            images = await _poll_until_done(client, alloc.email, gen_id)

            # Download all images for this generation concurrently
            async def download_one(img: dict) -> str:
                if img.get("status") == "failed":
                    raise RuntimeError(
                        f"Image failed on server: {img.get('errorMessage', 'unknown')}"
                    )
                idx = img.get("generationIndex", images.index(img)) + 1
                filename_hint = f"{task.img_id}_{idx}"
                out_path = out_dir / f"{filename_hint}.png"
                await _download_image(client, alloc.email, img["id"], filename_hint, out_path)
                return out_path.name

            saved = await asyncio.gather(*[download_one(img) for img in images])

            async with print_lock:
                counter[0] += 1
                print(f"  [{counter[0]}/{total_tasks}] {task.img_id} OK  saved: {list(saved)}")

        results = await asyncio.gather(
            *[handle_task(task) for task in alloc.tasks],
            return_exceptions=True,
        )

        for task, result in zip(alloc.tasks, results):
            if isinstance(result, Exception):
                async with print_lock:
                    print(f"  {task.img_id} FAIL  ERROR: {result}")
                errors.append((task.img_id, str(result)))

    return errors


# ── Main ──────────────────────────────────────────────────────────────────────

async def async_main(args: argparse.Namespace) -> None:
    project_dir = Path(args.project).resolve()
    script_dir = project_dir / "script"
    out_dir = project_dir / "assets" / "images"

    if not script_dir.exists():
        print(f"ERROR: script/ not found in {project_dir}", file=sys.stderr)
        sys.exit(1)

    # ── 1. Parse prompts ──────────────────────────────────────────────────────
    all_tasks = parse_image_prompts(script_dir)
    print(f"\nParsed {len(all_tasks)} prompts from image-prompts.md")

    if args.img:
        all_tasks = [t for t in all_tasks if t.img_id == args.img]
        if not all_tasks:
            print(f"ERROR: '{args.img}' not found in image-prompts.md", file=sys.stderr)
            sys.exit(1)

    out_dir.mkdir(parents=True, exist_ok=True)

    tasks = all_tasks if args.overwrite else find_missing_tasks(all_tasks, out_dir)
    done_count = len(all_tasks) - len(tasks)

    print(f"Status  : {done_count} done | {len(tasks)} to generate")

    if not tasks:
        print("\nAll images already generated. Use --overwrite to regenerate.")
        return

    # ── 2. Fetch valid accounts ───────────────────────────────────────────────
    print(f"\nRegistrar: {BASE_URL}")
    print("Fetching valid AA accounts...")

    async with httpx.AsyncClient() as client:
        accounts = await fetch_valid_accounts(client)

    if not accounts:
        print("ERROR: No valid AA accounts found (check_status=valid, not disabled).", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(accounts)} valid accounts. Fetching live balances...")

    # ── 3. Fetch balances concurrently ────────────────────────────────────────
    async with httpx.AsyncClient() as client:
        bal_sem = asyncio.Semaphore(10)  # max 10 concurrent AA session checks
        balance_results = await asyncio.gather(
            *[fetch_balance(client, a["email"], bal_sem) for a in accounts],
            return_exceptions=True,
        )

    balances: dict[str, float] = {}
    for acc, result in zip(accounts, balance_results):
        if isinstance(result, Exception):
            print(f"  [WARN] {acc['email']}: failed to fetch balance — {result}")
        else:
            balances[acc["email"]] = result
            print(f"  {acc['email']}: ${result:.3f}")

    eligible_count = sum(1 for b in balances.values() if b >= COST_PER_PROMPT)
    print(f"\n{eligible_count}/{len(balances)} accounts eligible (balance >= ${COST_PER_PROMPT:.3f}/prompt)")

    # ── 4. Greedy fill ────────────────────────────────────────────────────────
    allocs, unassigned = greedy_fill(tasks, balances)

    if not allocs:
        print(
            "ERROR: No accounts with sufficient credit.",
            f"Need ${COST_PER_PROMPT:.3f} per prompt.",
            file=sys.stderr,
        )
        sys.exit(1)

    total_assigned = sum(len(a.tasks) for a in allocs)
    total_cost = total_assigned * COST_PER_PROMPT

    print("\nGreedy fill plan (ascending balance -> drain smallest first):")
    print(f"  {'Account':<45} {'Balance':>9}  {'Capacity':>9}  {'Assigned':>9}")
    print("  " + "-" * 78)
    for a in allocs:
        print(f"  {a.email:<45} ${a.balance:>8.3f}  {a.capacity:>9}  {len(a.tasks):>9}")
    print()
    print(f"  Prompts assigned  : {total_assigned}/{len(tasks)}")
    print(f"  Estimated cost    : ${total_cost:.3f}")
    print(f"  Model             : Nano Banana 2 ({MODEL_ID[:8]}...)")
    print(f"  Dimensions        : {WIDTH}x{HEIGHT}  x{GENERATIONS_PER_MODEL} per prompt")

    if unassigned:
        print(f"\n  WARNING: {len(unassigned)} prompt(s) could NOT be assigned (total credit exhausted):")
        for t in unassigned:
            print(f"    - {t.img_id}: {t.prompt[:70]}...")

    if args.dry_run:
        print("\n[DRY RUN] Stopping here. Remove --dry-run to execute.")
        return

    # ── 5. Execute concurrently ───────────────────────────────────────────────
    print(f"\nGenerating {total_assigned} prompt(s) across {len(allocs)} account(s)...\n")

    print_lock = asyncio.Lock()
    counter = [0]  # shared progress counter — mutated under print_lock

    results = await asyncio.gather(
        *[process_account(a, out_dir, print_lock, total_assigned, counter) for a in allocs],
        return_exceptions=True,
    )

    # ── 6. Report ─────────────────────────────────────────────────────────────
    all_errors: list[tuple[str, str]] = []
    for r in results:
        if isinstance(r, Exception):
            all_errors.append(("<<account-level>>", str(r)))
        else:
            all_errors.extend(r)

    print(f"\n{'-' * 60}")
    print(f"Done.  Assigned={total_assigned}  Errors={len(all_errors)}  Unassigned={len(unassigned)}")

    if all_errors:
        print(f"\nFailed prompts ({len(all_errors)}):")
        for img_id, err in all_errors:
            print(f"  {img_id}: {err}")

    if unassigned:
        print(f"\nUnassigned prompts ({len(unassigned)}) — re-run after topping up credit:")
        for t in unassigned:
            print(f"  {t.img_id}: {t.prompt[:70]}...")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate images via AA accounts using greedy fill strategy",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--project", required=True, help="Path to project root (contains script/ and assets/)")
    parser.add_argument("--dry-run", action="store_true", help="Show distribution plan without generating")
    parser.add_argument("--img", default=None, help="Generate only this image ID (e.g. IMG-02-01)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing images")
    args = parser.parse_args()

    # ── Setup file logging ────────────────────────────────────────────────
    project_dir = Path(args.project).resolve()
    log_dir = project_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"gen_images_{datetime.now():%Y%m%d_%H%M%S}.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(message)s",
        datefmt="%H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_file, encoding="utf-8"),
        ],
    )
    log.info(f"Log file: {log_file}")

    # Redirect print() → log so everything is captured
    _orig_print = __builtins__["print"] if isinstance(__builtins__, dict) else print
    import builtins
    def _log_print(*args_p, **kwargs_p):
        msg = " ".join(str(a) for a in args_p)
        log.info(msg)
    builtins.print = _log_print

    try:
        asyncio.run(async_main(args))
    finally:
        builtins.print = _orig_print


if __name__ == "__main__":
    main()
