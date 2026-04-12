#!/usr/bin/env python3
"""
gen_audio.py — Generate TTS audio from script chunks via tts-proxy API.

FE only: parses script, calls tts-proxy for audio, saves WAV files.
NO Gemini API logic here — all key rotation and RPD tracking is in tts-proxy.

Usage:
    python gen_audio.py --project <path>            # generate all missing audio
    python gen_audio.py --project <path> --dry-run  # show what would be generated
    python gen_audio.py --project <path> --voice Charon
    python gen_audio.py --project <path> --chunk audio-00-01  # single chunk
    python gen_audio.py --project <path> --list     # list all chunks + status

Examples:
    python gen_audio.py --project d:/business/account-creation/content-vault/episodes/boring-history/ming-grain-storage-1450
    python gen_audio.py --project . --dry-run
"""

import argparse
import logging
import re
import sys
from datetime import datetime
from pathlib import Path

import httpx
import yaml

log = logging.getLogger("gen_audio")

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DEFAULT_PROXY_URL = "http://127.0.0.1:8700/api"


def _find_config() -> "Path | None":
    here = Path(__file__).resolve().parent
    for candidate in [here.parent / "config" / "tts.yaml", here / "config" / "tts.yaml"]:
        if candidate.exists():
            return candidate
    return None


def load_config(config_path=None) -> dict:
    path = config_path or _find_config()
    if path and Path(path).exists():
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}


CFG = load_config()

DEFAULT_VOICE = CFG.get("default_voice", "Charon")
SECTION_FILES = CFG.get("script", {}).get("section_files", [
    "00-intro.md", "01-structure.md", "02-quality.md", "03-incidents.md", "04-outro.md",
])

AUDIO_EXT = ".wav"

# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def extract_chunks(script_dir: Path, section_files: list) -> list:
    """Parse all section files and extract chunks.
    Returns list of {chunk_id, text, file} dicts.
    """
    chunks = []
    chunk_pattern = re.compile(r"^### CHUNK (audio-\d{2}-\d{2})", re.MULTILINE)

    for filename in section_files:
        filepath = script_dir / filename
        if not filepath.exists():
            print(f"  [skip] {filename} not found")
            continue

        content = filepath.read_text(encoding="utf-8")
        matches = list(chunk_pattern.finditer(content))

        for i, match in enumerate(matches):
            chunk_id = match.group(1)
            start = match.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
            raw = content[start:end]

            # Strip img comments, --- dividers, empty lines at start/end
            text = re.sub(r"<!--.*?-->", "", raw, flags=re.DOTALL)
            text = re.sub(r"^---+\s*$", "", text, flags=re.MULTILINE)
            text = text.strip()

            if text:
                chunks.append({"chunk_id": chunk_id, "text": text, "file": filename})

    return chunks


# ---------------------------------------------------------------------------
# TTS proxy call
# ---------------------------------------------------------------------------

def call_tts_proxy(text: str, voice: str, proxy_url: str, timeout: int = 120) -> bytes:
    """Call tts-proxy /api/tts endpoint. Returns WAV bytes.

    tts-proxy handles key rotation, RPD tracking, text splitting, and concatenation.
    """
    r = httpx.post(
        f"{proxy_url}/tts",
        json={"text": text, "voice_id": voice},
        timeout=timeout,
    )
    if r.status_code == 503:
        print(f"  PROXY: {r.json().get('detail', 'All keys exhausted daily quota')}")
        sys.exit(1)
    r.raise_for_status()
    return r.content


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate TTS audio via tts-proxy")
    parser.add_argument("--project", required=True, help="Path to project root (contains script/ and assets/)")
    parser.add_argument("--voice", default=DEFAULT_VOICE, help=f"Gemini voice name (default: {DEFAULT_VOICE})")
    parser.add_argument("--chunk", default=None, help="Generate only this chunk (e.g. audio-00-01)")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be generated without calling API")
    parser.add_argument("--list", action="store_true", dest="list_chunks", help="List all chunks and their output status")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing audio files")
    parser.add_argument("--proxy", default=DEFAULT_PROXY_URL, help=f"TTS proxy URL (default: {DEFAULT_PROXY_URL})")
    args = parser.parse_args()

    # Resolve paths
    project_dir = Path(args.project).resolve()
    script_dir = project_dir / "script"
    audio_dir = project_dir / "assets" / "audio"

    if not script_dir.exists():
        print(f"ERROR: script/ not found in {project_dir}")
        sys.exit(1)

    audio_dir.mkdir(parents=True, exist_ok=True)

    # Load section_files from project-local config if available
    local_cfg_path = project_dir / "config" / "tts.yaml"
    active_cfg = load_config(local_cfg_path) if local_cfg_path.exists() else CFG
    section_files = active_cfg.get("script", {}).get("section_files", SECTION_FILES)

    # Check proxy health
    try:
        health = httpx.get(f"{args.proxy}/health", timeout=5)
        health.raise_for_status()
        info = health.json()
        print(f"Proxy: {info.get('model', '?')}, keys={info.get('available_keys', '?')}, available_today={info.get('available_today', '?')}")
    except Exception as exc:
        print(f"ERROR: Cannot reach tts-proxy at {args.proxy}: {exc}")
        sys.exit(1)

    # Parse chunks
    chunks = extract_chunks(script_dir, section_files)
    if not chunks:
        print("ERROR: No chunks found in script files.")
        sys.exit(1)

    # Filter by --chunk if specified
    if args.chunk:
        chunks = [c for c in chunks if c["chunk_id"] == args.chunk]
        if not chunks:
            print(f"ERROR: chunk '{args.chunk}' not found")
            sys.exit(1)

    # --list mode
    if args.list_chunks:
        print(f"\n{'#':<4} {'Chunk':<16} {'File':<22} {'Words':<7} {'Status'}")
        print("-" * 70)
        for i, c in enumerate(chunks, 1):
            out = audio_dir / f"{c['chunk_id']}{AUDIO_EXT}"
            status = "OK exists" if out.exists() else "missing"
            words = len(c["text"].split())
            print(f"{i:<4} {c['chunk_id']:<16} {c['file']:<22} {words:<7} {status}")
        print(f"\nTotal: {len(chunks)} chunks")
        return

    # Filter out already-generated chunks (unless --overwrite)
    if not args.overwrite:
        before = len(chunks)
        chunks = [c for c in chunks if not (audio_dir / f"{c['chunk_id']}{AUDIO_EXT}").exists()]
        skipped = before - len(chunks)
        if skipped:
            print(f"  [skip] {skipped} chunks already exist (use --overwrite to regenerate)")

    if not chunks:
        print("All chunks already generated.")
        return

    if args.dry_run:
        print(f"\nDry run -- would generate {len(chunks)} chunks:")
        for c in chunks:
            print(f"  {c['chunk_id']} ({len(c['text'])} chars)")
        return

    # ── Setup file logging ────────────────────────────────────────────────
    log_dir = project_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"gen_audio_{datetime.now():%Y%m%d_%H%M%S}.log"

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

    import builtins
    def _log_print(*args_p, **kwargs_p):
        msg = " ".join(str(a) for a in args_p)
        log.info(msg)
    builtins.print = _log_print

    # Generate — sequential to respect RPD limits
    print(f"\nGenerating {len(chunks)} chunk(s) with voice={args.voice}")
    print(f"Output: {audio_dir}\n")

    success = 0
    failed = 0

    for i, c in enumerate(chunks, 1):
        chunk_id = c["chunk_id"]
        out_path = audio_dir / f"{chunk_id}{AUDIO_EXT}"
        try:
            wav_bytes = call_tts_proxy(c["text"], args.voice, args.proxy)
            out_path.write_bytes(wav_bytes)
            success += 1
            print(f"  [{i}/{len(chunks)}] OK {chunk_id}  ({len(wav_bytes):,} bytes)")
        except httpx.HTTPStatusError as exc:
            failed += 1
            print(f"  [{i}/{len(chunks)}] FAIL {chunk_id}  HTTP {exc.response.status_code}: {exc.response.text[:200]}")
        except Exception as exc:
            failed += 1
            print(f"  [{i}/{len(chunks)}] FAIL {chunk_id}  {exc}")

    print(f"\nDone: {success} generated, {failed} failed.")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()