#!/usr/bin/env python3
"""
gen_full_flow.py — Run complete pipeline: folders → TTS → Images → Clips.

One command to generate everything:
    python gen_full_flow.py --project <path>

Or step by step:
    python gen_full_flow.py --project <path> --step tts
    python gen_full_flow.py --project <path> --step images
    python gen_full_flow.py --project <path> --step clips

Steps:
  1. folders  — Create assets/{audio,images,clips,thumbnails}/
  2. tts      — Generate audio from script (gen_audio.py logic)
  3. images   — Generate images from prompts (gen_images.py logic)
  4. clips    — Merge audio+images into video clips (gen_clips.py logic)
"""

import argparse
import asyncio
import json
import logging
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import httpx
import yaml

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DEFAULT_TTS_PROXY = "http://127.0.0.1:8700/api"
DEFAULT_AA_PROXY = "http://127.0.0.1:8709"
DEFAULT_VOICE = "Charon"
AUDIO_EXT = ".wav"
CLIP_TAIL_SILENCE = 1.0

log = logging.getLogger("gen_full_flow")


# ---------------------------------------------------------------------------
# Project Structure
# ---------------------------------------------------------------------------

def ensure_folders(project_dir: Path) -> dict[Path, str]:
    """Create all required asset folders. Returns {path: description}."""
    folders = {
        project_dir / "assets" / "audio": "TTS audio files",
        project_dir / "assets" / "images": "AI generated images",
        project_dir / "assets" / "clips": "Video clips (audio+image)",
        project_dir / "assets" / "thumbnails": "Thumbnail images (manual)",
        project_dir / "logs": "Generation logs",
        project_dir / "config": "Episode config",
    }
    for folder, desc in folders.items():
        folder.mkdir(parents=True, exist_ok=True)
        log.info(f"[folders] {folder.name}/ — {desc}")
    return folders


# ---------------------------------------------------------------------------
# Config Loading
# ---------------------------------------------------------------------------

def load_config(project_dir: Path) -> dict:
    """Load episode-specific config if exists, else empty."""
    cfg_path = project_dir / "config" / "tts.yaml"
    if cfg_path.exists():
        with open(cfg_path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}


# ---------------------------------------------------------------------------
# Step 0: Validate Prompts
# ---------------------------------------------------------------------------

def step_check_prompts(project_dir: Path) -> bool:
    """Validate image prompts before generation. Returns True if all valid."""
    prompts_file = project_dir / "script" / "image-prompts.md"
    if not prompts_file.exists():
        log.error("[check] image-prompts.md not found")
        return False

    text = prompts_file.read_text(encoding="utf-8")
    prompts = []

    # Parse all prompts (same logic as check_prompts.py)
    for m in re.finditer(r"^(IMG-\d{2}-\d{2})(?:\s*\[TITLE\])?:\s*(.+)$", text, re.MULTILINE):
        prompts.append({"id": m.group(1), "text": m.group(2).strip(), "length": len(m.group(2).strip())})

    for m in re.finditer(
        r"^### (IMG-\d{2}-\d{2})(?:\s*\[TITLE\])?\b.*?\n```\n(.*?)\n```",
        text, re.MULTILINE | re.DOTALL,
    ):
        pt = " ".join(m.group(2).split())
        prompts.append({"id": m.group(1), "text": pt, "length": len(pt)})

    heading_pattern = re.compile(
        r"^### (IMG-\d{2}-\d{2})(?:\s*\[TITLE\])?\s*$\n(.+?)(?=\n###|\n---|\n##|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    seen = {p["id"] for p in prompts}
    for m in heading_pattern.finditer(text):
        if m.group(1) not in seen:
            pt = " ".join(m.group(2).split())
            prompts.append({"id": m.group(1), "text": pt, "length": len(pt)})

    if not prompts:
        log.error("[check] No prompts found")
        return False

    log.info(f"[check] Found {len(prompts)} prompts")

    # Check uniqueness
    seen_ids = {}
    duplicates = []
    for p in prompts:
        if p["id"] in seen_ids:
            duplicates.append(p["id"])
        seen_ids[p["id"]] = True

    if duplicates:
        log.error(f"[check] Duplicate IDs: {duplicates}")
        return False

    # Check lengths
    short = [p for p in prompts if p["length"] < 200]
    long = [p for p in prompts if p["length"] > 299]

    if short:
        for p in short:
            log.warning(f"[check] {p['id']}: TOO SHORT ({p['length']} chars)")
    if long:
        for p in long:
            log.warning(f"[check] {p['id']}: TOO LONG ({p['length']} chars, +{p['length']-299})")

    if short or long:
        log.error(f"[check] Validation failed: {len(short)} short, {len(long)} long")
        return False

    log.info("[check] All prompts valid (200-299 chars)")
    return True


# ---------------------------------------------------------------------------
# Step 1: TTS Generation
# ---------------------------------------------------------------------------

def parse_chunks(script_dir: Path, section_files: list) -> list:
    """Parse all section files and extract audio chunks."""
    chunks = []
    chunk_pattern = re.compile(r"^### CHUNK (audio-\d{2}-\d{2})", re.MULTILINE)

    for filename in section_files:
        filepath = script_dir / filename
        if not filepath.exists():
            log.warning(f"[tts] {filename} not found, skipping")
            continue

        content = filepath.read_text(encoding="utf-8")
        matches = list(chunk_pattern.finditer(content))

        for i, match in enumerate(matches):
            chunk_id = match.group(1)
            start = match.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
            raw = content[start:end]

            text = re.sub(r"<!--.*?-->", "", raw, flags=re.DOTALL)
            text = re.sub(r"^---+\s*$", "", text, flags=re.MULTILINE)
            text = text.strip()

            if text:
                chunks.append({"chunk_id": chunk_id, "text": text, "file": filename})

    return chunks


def call_tts_proxy(text: str, voice: str, proxy_url: str) -> bytes:
    """Call tts-proxy /api/tts endpoint. Returns WAV bytes."""
    r = httpx.post(
        f"{proxy_url}/tts",
        json={"text": text, "voice_id": voice},
        timeout=120,
    )
    if r.status_code == 503:
        raise RuntimeError(f"TTS proxy: all keys exhausted daily quota")
    r.raise_for_status()
    return r.content


def step_tts(project_dir: Path, cfg: dict, proxy_url: str) -> tuple[int, int]:
    """Generate TTS audio. Returns (success_count, fail_count)."""
    script_dir = project_dir / "script"
    audio_dir = project_dir / "assets" / "audio"

    section_files = cfg.get("script", {}).get("section_files", [])
    if not section_files:
        log.error("[tts] No section_files in config/tts.yaml")
        return 0, 0

    voice = cfg.get("default_voice", DEFAULT_VOICE)
    chunks = parse_chunks(script_dir, section_files)

    if not chunks:
        log.error("[tts] No chunks found")
        return 0, 0

    log.info(f"[tts] Found {len(chunks)} chunks to generate")

    # Check existing
    pending = [c for c in chunks if not (audio_dir / f"{c['chunk_id']}{AUDIO_EXT}").exists()]
    existing = len(chunks) - len(pending)
    if existing:
        log.info(f"[tts] {existing} chunks already exist, skipping")

    if not pending:
        log.info("[tts] All chunks already generated")
        return 0, 0

    # Check proxy health
    try:
        health = httpx.get(f"{proxy_url}/health", timeout=5)
        health.raise_for_status()
        info = health.json()
        log.info(f"[tts] Proxy ready: {info.get('available_keys', '?')} keys, {info.get('available_today', '?')} today")
    except Exception as exc:
        log.error(f"[tts] Cannot reach proxy: {exc}")
        return 0, len(pending)

    success, failed = 0, 0
    for i, c in enumerate(pending, 1):
        chunk_id = c["chunk_id"]
        out_path = audio_dir / f"{chunk_id}{AUDIO_EXT}"
        try:
            wav_bytes = call_tts_proxy(c["text"], voice, proxy_url)
            out_path.write_bytes(wav_bytes)
            success += 1
            log.info(f"[tts] [{i}/{len(pending)}] {chunk_id} OK ({len(wav_bytes):,} bytes)")
        except Exception as exc:
            failed += 1
            log.error(f"[tts] [{i}/{len(pending)}] {chunk_id} FAIL: {exc}")

    log.info(f"[tts] Done: {success} success, {failed} failed")
    return success, failed


# ---------------------------------------------------------------------------
# Step 2: Image Generation
# ---------------------------------------------------------------------------

from dataclasses import dataclass, field

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


def parse_image_prompts(script_dir: Path) -> list[PromptTask]:
    """Parse image-prompts.md and return list of PromptTask."""
    prompts_file = script_dir / "image-prompts.md"
    if not prompts_file.exists():
        raise FileNotFoundError(f"image-prompts.md not found in {script_dir}")

    content = prompts_file.read_text(encoding="utf-8")

    # Extract metadata
    meta = {}
    for m in re.finditer(r"<!--\s*(style-suffix|title-suffix):\s*(.+?)\s*-->", content):
        meta[m.group(1)] = m.group(2).strip()
    style_suffix = meta.get("style-suffix", "")
    title_suffix = meta.get("title-suffix", "")

    # Extract [TITLE] marked IDs
    title_ids: set[str] = set()
    for m in re.finditer(r"(IMG-\d{2}-\d{2})\s*\[TITLE\]", content):
        title_ids.add(m.group(1))

    # Parse all formats
    matches: list[tuple[int, str, str]] = []

    for m in re.finditer(r"^(IMG-\d{2}-\d{2})(?:\s*\[TITLE\])?:\s*(.+)$", content, re.MULTILINE):
        matches.append((m.start(), m.group(1), m.group(2).strip()))

    for m in re.finditer(
        r"^### (IMG-\d{2}-\d{2})(?:\s*\[TITLE\])?\b.*?\n```\n(.*?)\n```",
        content, re.MULTILINE | re.DOTALL,
    ):
        matches.append((m.start(), m.group(1), " ".join(m.group(2).split())))

    heading_pattern = re.compile(
        r"^### (IMG-\d{2}-\d{2})(?:\s*\[TITLE\])?\s*$\n(.+?)(?=\n###|\n---|\n##|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    already_matched = {pos for pos, _, _ in matches}
    for m in heading_pattern.finditer(content):
        if m.start() not in already_matched:
            matches.append((m.start(), m.group(1), " ".join(m.group(2).split())))

    tasks = []
    for _, img_id, prompt_text in matches:
        parts = [prompt_text]
        if style_suffix:
            parts.append(style_suffix)
        if img_id in title_ids and title_suffix:
            parts.append(title_suffix)
        final = ", ".join(parts)
        tasks.append(PromptTask(img_id=img_id, prompt=final))

    return tasks


async def fetch_valid_accounts(client: httpx.AsyncClient, base_url: str) -> list[dict]:
    r = await client.get(f"{base_url}/api/v1/accounts", params={"service": "ARTIFICIALANALYSIS"})
    r.raise_for_status()
    data = r.json()["data"]
    return [a for a in data if not a.get("disabled") and a.get("check_status") == "valid"]


async def fetch_balance(client: httpx.AsyncClient, base_url: str, email: str) -> float:
    r = await client.get(f"{base_url}/api/v1/aa/session", params={"email": email})
    r.raise_for_status()
    data = r.json()["data"]
    terms = data.get("user", {}).get("termsOfUseAcceptedAt")
    if terms is None:
        raise RuntimeError("Terms not accepted")
    return float(data.get("org", {}).get("balance", 0))


def greedy_fill(tasks: list[PromptTask], balances: dict[str, float], cost: float) -> list[AccountAlloc]:
    eligible = [(e, b) for e, b in balances.items() if b >= cost]
    eligible.sort(key=lambda x: x[1])  # ascending

    allocs = []
    remaining = list(tasks)
    for email, balance in eligible:
        if not remaining:
            break
        cap = int(balance / cost)
        if cap <= 0:
            continue
        batch = remaining[:cap]
        remaining = remaining[cap:]
        allocs.append(AccountAlloc(email=email, balance=balance, capacity=cap, tasks=batch))
    return allocs


async def process_images_for_account(
    alloc: AccountAlloc,
    out_dir: Path,
    base_url: str,
    model_id: str,
    print_lock: asyncio.Lock,
    counter: list[int],
    total: int,
) -> list[tuple[str, str]]:
    """Generate images for one account. Returns list of (img_id, error)."""
    errors = []

    async with httpx.AsyncClient() as client:
        for task in alloc.tasks:
            max_retries = 3
            base_delay = 2.0
            for attempt in range(1, max_retries + 1):
                try:
                    # Generate
                    r = await client.post(
                        f"{base_url}/api/v1/aa/generate",
                        json={
                            "email": alloc.email,
                            "prompt": task.prompt,
                            "model_ids": [model_id],
                            "generations_per_model": 1,
                            "width": 1920,
                            "height": 1080,
                        },
                        timeout=60,
                    )
                    r.raise_for_status()
                    data = r.json()["data"]
                    gen_id = data.get("generationId") or data.get("id")

                    async with print_lock:
                        log.info(f"[images] [~/{total}] {task.img_id} @{alloc.email.split('@')[0]} gen={gen_id[:8]}...")

                    # Poll
                    while True:
                        await asyncio.sleep(3)
                        r = await client.get(
                            f"{base_url}/api/v1/aa/generation/{gen_id}",
                            params={"email": alloc.email},
                            timeout=30,
                        )
                        r.raise_for_status()
                        imgs = r.json()["data"].get("images", [])
                        if all(img.get("status") != "pending" for img in imgs):
                            break

                    # Download
                    for img in imgs:
                        if img.get("status") == "failed":
                            raise RuntimeError(f"Image failed: {img.get('errorMessage')}")
                        idx = imgs.index(img) + 1
                        filename = f"{task.img_id}_{idx}"
                        r = await client.post(
                            f"{base_url}/api/v1/aa/image-download",
                            json={"email": alloc.email, "image_id": img["id"], "filename_hint": filename},
                            timeout=60,
                        )
                        r.raise_for_status()
                        out_path = out_dir / f"{filename}.png"
                        out_path.write_bytes(r.content)

                    async with print_lock:
                        counter[0] += 1
                        log.info(f"[images] [{counter[0]}/{total}] {task.img_id} OK")
                    break  # Success, exit retry loop

                except (httpx.HTTPStatusError, httpx.ConnectError) as exc:
                    if attempt < max_retries:
                        delay = base_delay * (2 ** (attempt - 1))
                        async with print_lock:
                            log.warning(f"[images] {task.img_id} attempt {attempt} failed, retry in {delay}s")
                        await asyncio.sleep(delay)
                    else:
                        errors.append((task.img_id, str(exc)))
                        async with print_lock:
                            log.error(f"[images] {task.img_id} FAIL: {exc}")
                except Exception as exc:
                    errors.append((task.img_id, str(exc)))
                    async with print_lock:
                        log.error(f"[images] {task.img_id} FAIL: {exc}")
                    break

    return errors


async def step_images(project_dir: Path, base_url: str) -> tuple[int, int]:
    """Generate images. Returns (success_count, fail_count)."""
    script_dir = project_dir / "script"
    images_dir = project_dir / "assets" / "images"

    try:
        all_tasks = parse_image_prompts(script_dir)
    except Exception as exc:
        log.error(f"[images] Failed to parse prompts: {exc}")
        return 0, 0

    log.info(f"[images] Parsed {len(all_tasks)} prompts")

    # Find missing
    pending = []
    for task in all_tasks:
        if not (images_dir / f"{task.img_id}_1.png").exists():
            pending.append(task)

    existing = len(all_tasks) - len(pending)
    if existing:
        log.info(f"[images] {existing} already exist, skipping")

    if not pending:
        log.info("[images] All images already generated")
        return 0, 0

    log.info(f"[images] {len(pending)} to generate")

    # Fetch accounts
    async with httpx.AsyncClient() as client:
        accounts = await fetch_valid_accounts(client, base_url)
        if not accounts:
            log.error("[images] No valid AA accounts")
            return 0, len(pending)

        # Fetch balances
        balances = {}
        for acc in accounts:
            try:
                bal = await fetch_balance(client, base_url, acc["email"])
                balances[acc["email"]] = bal
            except Exception as exc:
                log.warning(f"[images] Failed to get balance for {acc['email']}: {exc}")

    cost_per_prompt = 0.144  # Nano Banana 2
    eligible = sum(1 for b in balances.values() if b >= cost_per_prompt)
    log.info(f"[images] {eligible}/{len(balances)} accounts eligible")

    allocs = greedy_fill(pending, balances, cost_per_prompt)
    if not allocs:
        log.error(f"[images] No accounts with sufficient credit (need ${cost_per_prompt:.3f}/prompt)")
        return 0, len(pending)

    total_assigned = sum(len(a.tasks) for a in allocs)
    log.info(f"[images] Assigned {total_assigned} prompts across {len(allocs)} accounts")

    # Execute
    print_lock = asyncio.Lock()
    counter = [0]
    results = await asyncio.gather(*[
        process_images_for_account(a, images_dir, base_url, "c3f4bea0-4cbf-49ea-b8ea-0b9d917ebc0c",
                                   print_lock, counter, total_assigned)
        for a in allocs
    ])

    all_errors = []
    for r in results:
        all_errors.extend(r)

    success = total_assigned - len(all_errors)
    log.info(f"[images] Done: {success} success, {len(all_errors)} failed")
    return success, len(all_errors)


# ---------------------------------------------------------------------------
# Step 3: Clip Generation
# ---------------------------------------------------------------------------

def get_audio_duration(audio_path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "json", str(audio_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)
    return float(data["format"]["duration"])


def build_clip(audio: Path, image: Path, output: Path) -> None:
    """Build static clip: image + audio + tail silence."""
    duration = get_audio_duration(audio)
    total = duration + CLIP_TAIL_SILENCE

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-t", str(total), "-i", str(image),
        "-i", str(audio),
        "-filter_complex", f"[1:a]apad=pad_dur={CLIP_TAIL_SILENCE}[a]",
        "-map", "0:v", "-map", "[a]",
        "-c:v", "libx264", "-tune", "stillimage",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-t", str(total), str(output),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {result.stderr[-500:]}")


def step_clips(project_dir: Path) -> tuple[int, int]:
    """Generate video clips. Returns (success_count, fail_count)."""
    script_dir = project_dir / "script"
    audio_dir = project_dir / "assets" / "audio"
    images_dir = project_dir / "assets" / "images"
    clips_dir = project_dir / "assets" / "clips"

    # Parse audio-image map
    map_file = script_dir / "audio-image-map.md"
    if not map_file.exists():
        log.error("[clips] audio-image-map.md not found")
        return 0, 0

    # Simple parsing for 4-column table
    row_pattern = re.compile(r"^\|\s*(audio-\d+-\d+)\s*\|[^|]*\|\s*(IMG-\d+-\d+)\s*\|")
    rows = []
    for line in map_file.read_text(encoding="utf-8").splitlines():
        m = row_pattern.match(line)
        if m:
            rows.append({"audio_id": m.group(1), "image_id": m.group(2)})

    if not rows:
        log.error("[clips] No rows parsed from audio-image-map.md")
        return 0, 0

    log.info(f"[clips] Found {len(rows)} clips to generate")

    # Find pending
    pending = []
    for row in rows:
        clip_name = f"clip-{row['image_id']}.mp4"
        if not (clips_dir / clip_name).exists():
            pending.append(row)

    existing = len(rows) - len(pending)
    if existing:
        log.info(f"[clips] {existing} already exist, skipping")

    if not pending:
        log.info("[clips] All clips already generated")
        return 0, 0

    clips_dir.mkdir(parents=True, exist_ok=True)

    success, failed = 0, 0
    for i, row in enumerate(pending, 1):
        audio_id = row["audio_id"]
        image_id = row["image_id"]
        audio = audio_dir / f"{audio_id}{AUDIO_EXT}"
        image = images_dir / f"{image_id}_1.png"
        output = clips_dir / f"clip-{image_id}.mp4"

        log.info(f"[clips] [{i}/{len(pending)}] clip-{image_id}.mp4 ...")

        if not audio.exists():
            log.error(f"[clips] Audio not found: {audio}")
            failed += 1
            continue
        if not image.exists():
            log.error(f"[clips] Image not found: {image}")
            failed += 1
            continue

        try:
            build_clip(audio, image, output)
            size_mb = output.stat().st_size / 1_048_576
            log.info(f"[clips] [{i}/{len(pending)}] OK ({size_mb:.1f} MB)")
            success += 1
        except Exception as exc:
            log.error(f"[clips] [{i}/{len(pending)}] FAILED: {exc}")
            failed += 1

    log.info(f"[clips] Done: {success} success, {failed} failed")
    return success, failed


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def setup_logging(log_dir: Path) -> Path:
    """Setup logging to file and console."""
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"gen_full_flow_{datetime.now():%Y%m%d_%H%M%S}.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(message)s",
        datefmt="%H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_file, encoding="utf-8"),
        ],
    )
    return log_file


def main():
    parser = argparse.ArgumentParser(description="Full pipeline: folders → TTS → Images → Clips")
    parser.add_argument("--project", required=True, help="Path to episode directory")
    parser.add_argument("--step", choices=["folders", "tts", "images", "clips", "all"],
                        default="all", help="Run specific step (default: all)")
    parser.add_argument("--tts-proxy", default=DEFAULT_TTS_PROXY, help="TTS proxy URL")
    parser.add_argument("--aa-proxy", default=DEFAULT_AA_PROXY, help="AA proxy URL")
    args = parser.parse_args()

    project_dir = Path(args.project).resolve()
    if not project_dir.exists():
        print(f"ERROR: Project not found: {project_dir}", file=sys.stderr)
        sys.exit(1)

    log_file = setup_logging(project_dir / "logs")
    log.info(f"=" * 60)
    log.info(f"gen_full_flow — Project: {project_dir.name}")
    log.info(f"Log: {log_file}")
    log.info(f"=" * 60)

    cfg = load_config(project_dir)

    # Run steps
    total_success, total_fail = 0, 0

    if args.step in ("folders", "all"):
        log.info("\n" + "-" * 60)
        log.info("STEP 1: Creating folders")
        ensure_folders(project_dir)

    if args.step in ("tts", "all"):
        log.info("\n" + "-" * 60)
        log.info("STEP 2: TTS Generation")
        s, f = step_tts(project_dir, cfg, args.tts_proxy)
        total_success += s
        total_fail += f

    if args.step in ("images", "all"):
        log.info("\n" + "-" * 60)
        log.info("STEP 3: Image Generation")
        s, f = asyncio.run(step_images(project_dir, args.aa_proxy))
        total_success += s
        total_fail += f

    if args.step in ("clips", "all"):
        log.info("\n" + "-" * 60)
        log.info("STEP 4: Clip Generation")
        s, f = step_clips(project_dir)
        total_success += s
        total_fail += f

    # Summary
    log.info("\n" + "=" * 60)
    log.info("FINAL SUMMARY")
    log.info(f"=" * 60)
    log.info(f"Total Success: {total_success}")
    log.info(f"Total Failed:  {total_fail}")
    log.info(f"Log saved to:  {log_file}")

    if total_fail > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
