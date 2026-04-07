#!/usr/bin/env python3
"""
gen_audio.py — Generate TTS audio from script chunks using Inworld AI API.

Usage:
    python gen_audio.py --project <path>           # generate all missing audio
    python gen_audio.py --project <path> --dry-run  # show what would be generated
    python gen_audio.py --project <path> --voice Graham --speed 0.85
    python gen_audio.py --project <path> --chunk audio-00-01  # single chunk
    python gen_audio.py --project <path> --list    # list all chunks + status

Examples:
    python gen_audio.py --project d:/business/content-vault/videos/boring-history/ming-grain-storage-1450
    python gen_audio.py --project . --dry-run
"""

import argparse
import base64
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Lock

import requests
import yaml

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
# Config file is at <workspace_root>/config/tts.yaml
# Walk up from this script's location to find it
def _find_config() -> Path:
    here = Path(__file__).resolve().parent
    for candidate in [here.parent / "config" / "tts.yaml", here / "config" / "tts.yaml"]:
        if candidate.exists():
            return candidate
    return None


def load_config(config_path: Path = None) -> dict:
    path = config_path or _find_config()
    if path and path.exists():
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}


CFG = load_config()

API_URL        = CFG.get("api", {}).get("url", "https://api.inworld.ai/tts/v1/voice")
API_KEY_ENV    = CFG.get("api", {}).get("key_env", "INWORLD_API_KEY")
DEFAULT_MODEL  = CFG.get("model", {}).get("id", "inworld-tts-1.5-max")
DEFAULT_VOICE  = CFG.get("voice", {}).get("id", "Graham")
DEFAULT_SPEED  = CFG.get("voice", {}).get("speed", 0.85)
DEFAULT_TEMP   = CFG.get("voice", {}).get("temperature", 0.9)
DEFAULT_WORKERS= CFG.get("generation", {}).get("workers", 4)
MAX_CHARS      = CFG.get("generation", {}).get("max_chars_per_request", 1900)
AUDIO_ENCODING = CFG.get("output", {}).get("audio_encoding", "MP3")
SAMPLE_RATE    = CFG.get("output", {}).get("sample_rate_hertz", 44100)
SECTION_FILES  = CFG.get("script", {}).get("section_files", [
    "00-intro.md", "01-structure.md", "02-quality.md", "03-incidents.md", "04-outro.md",
])


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------
def extract_chunks(script_dir: Path) -> list[dict]:
    """
    Parse all section files and extract chunks.
    Returns list of {chunk_id, text, file} dicts.
    """
    chunks = []
    chunk_pattern = re.compile(r"^### CHUNK (audio-\d{2}-\d{2})", re.MULTILINE)

    for filename in SECTION_FILES:
        filepath = script_dir / filename
        if not filepath.exists():
            print(f"  [skip] {filename} not found")
            continue

        content = filepath.read_text(encoding="utf-8")
        matches = list(chunk_pattern.finditer(content))

        for i, match in enumerate(matches):
            chunk_id = match.group(1)
            # Text starts after the chunk header line + optional img comment
            start = match.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
            raw = content[start:end]

            # Strip img comment, --- dividers, empty lines at start/end
            text = re.sub(r"<!--.*?-->", "", raw, flags=re.DOTALL)
            text = re.sub(r"^---+\s*$", "", text, flags=re.MULTILINE)
            text = text.strip()

            if text:
                chunks.append({"chunk_id": chunk_id, "text": text, "file": filename})

    return chunks


# ---------------------------------------------------------------------------
# API call
# ---------------------------------------------------------------------------
def split_text(text: str, max_chars: int = MAX_CHARS) -> list[str]:
    """
    Split text into parts <= max_chars, splitting at sentence boundaries ('. ').
    Tries to keep splits clean — never mid-sentence.
    """
    if len(text) <= max_chars:
        return [text]

    parts = []
    remaining = text

    while len(remaining) > max_chars:
        # Find last sentence end before max_chars
        window = remaining[:max_chars]
        # Try '. ' boundary (end of sentence followed by space)
        cut = window.rfind(". ")
        if cut == -1:
            # Fallback: split at last space
            cut = window.rfind(" ")
        if cut == -1:
            cut = max_chars  # hard cut as last resort

        parts.append(remaining[: cut + 1].strip())
        remaining = remaining[cut + 1:].strip()

    if remaining:
        parts.append(remaining)

    return parts


def synthesize(text: str, voice: str, model: str, speed: float, temperature: float, api_key: str) -> bytes:
    """Call Inworld TTS API. Returns raw MP3 bytes."""
    headers = {
        "Authorization": f"Basic {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "voiceId": voice,
        "modelId": model,
        "audioConfig": {
            "audioEncoding": AUDIO_ENCODING,
            "sampleRateHertz": SAMPLE_RATE,
            "speakingRate": speed,
        },
        "temperature": temperature,
        "applyTextNormalization": "ON",
    }

    resp = requests.post(API_URL, json=payload, headers=headers, timeout=120)

    if resp.status_code != 200:
        try:
            err = resp.json()
        except Exception:
            err = resp.text
        raise RuntimeError(f"API error {resp.status_code}: {err}")

    result = resp.json()
    return base64.b64decode(result["audioContent"])


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Generate TTS audio from script chunks")
    parser.add_argument("--project", required=True, help="Path to project root (contains script/ and assets/)")
    parser.add_argument("--voice", default=DEFAULT_VOICE, help=f"Inworld voiceId (default: {DEFAULT_VOICE})")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Model ID (default: {DEFAULT_MODEL})")
    parser.add_argument("--speed", type=float, default=DEFAULT_SPEED, help=f"Speaking rate 0.5–1.5 (default: {DEFAULT_SPEED})")
    parser.add_argument("--temperature", type=float, default=DEFAULT_TEMP, help=f"Temperature (default: {DEFAULT_TEMP})")
    parser.add_argument("--chunk", default=None, help="Generate only this chunk (e.g. audio-00-01)")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be generated without calling API")
    parser.add_argument("--list", action="store_true", help="List all chunks and their output status")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing audio files")
    parser.add_argument("--key", default=None, help=f"Inworld API key (or set {API_KEY_ENV} env var)")
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS, help=f"Parallel workers (default: {DEFAULT_WORKERS})")
    args = parser.parse_args()

    # Resolve paths
    project_dir = Path(args.project).resolve()
    script_dir = project_dir / "script"
    audio_dir = project_dir / "assets" / "audio"

    if not script_dir.exists():
        print(f"ERROR: script/ not found in {project_dir}")
        sys.exit(1)

    audio_dir.mkdir(parents=True, exist_ok=True)

    # API key
    api_key = args.key or os.environ.get(API_KEY_ENV, "")
    if not api_key and not args.dry_run and not args.list:
        print("ERROR: No API key. Set INWORLD_API_KEY env var or pass --key")
        sys.exit(1)

    # Parse chunks
    chunks = extract_chunks(script_dir)
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
    if args.list:
        print(f"\n{'#':<4} {'Chunk':<16} {'File':<22} {'Words':<7} {'Status'}")
        print("-" * 70)
        for i, c in enumerate(chunks, 1):
            out_file = audio_dir / f"{c['chunk_id']}.mp3"
            status = "exists" if out_file.exists() else "missing"
            word_count = len(c["text"].split())
            print(f"{i:<4} {c['chunk_id']:<16} {c['file']:<22} {word_count:<7} {status}")
        print(f"\nTotal: {len(chunks)} chunks | Audio dir: {audio_dir}")
        return

    # Summary
    missing = [c for c in chunks if not (audio_dir / f"{c['chunk_id']}.mp3").exists()]
    to_generate = chunks if args.overwrite else missing

    print(f"\nProject : {project_dir}")
    print(f"Voice   : {args.voice}  |  Model: {args.model}  |  Speed: {args.speed}  |  Temp: {args.temperature}")
    print(f"Output  : {audio_dir}")
    print(f"Chunks  : {len(chunks)} total | {len(missing)} missing | {len(to_generate)} to generate")

    if not to_generate:
        print("\nAll chunks already generated. Use --overwrite to regenerate.")
        return

    if args.dry_run:
        print("\n[DRY RUN] Would generate:")
        for c in to_generate:
            word_count = len(c["text"].split())
            print(f"  {c['chunk_id']}.mp3  ({word_count} words)  <- {c['file']}")
            # Show first 80 chars of text
            preview = c["text"][:80].replace("\n", " ")
            print(f"    \"{preview}...\"")
        return

    # Generate
    print()
    errors = []
    print_lock = Lock()
    counter = [0]  # mutable container for nonlocal-style counter

    def generate_chunk(i_chunk):
        i, chunk = i_chunk
        out_file = audio_dir / f"{chunk['chunk_id']}.mp3"
        word_count = len(chunk["text"].split())
        text = chunk["text"]

        try:
            t0 = time.time()
            parts = split_text(text)
            split_note = f"  (split into {len(parts)} parts)" if len(parts) > 1 else ""

            audio_bytes = b""
            for part in parts:
                audio_bytes += synthesize(
                    text=part,
                    voice=args.voice,
                    model=args.model,
                    speed=args.speed,
                    temperature=args.temperature,
                    api_key=api_key,
                )

            elapsed = time.time() - t0
            out_file.write_bytes(audio_bytes)
            size_kb = len(audio_bytes) / 1024
            with print_lock:
                counter[0] += 1
                print(f"[{counter[0]}/{len(to_generate)}] {chunk['chunk_id']}  ({word_count} words){split_note}  {size_kb:.0f}KB  ({elapsed:.1f}s)")
            return None
        except Exception as e:
            with print_lock:
                counter[0] += 1
                print(f"[{counter[0]}/{len(to_generate)}] {chunk['chunk_id']}  ERROR: {e}")
            return (chunk["chunk_id"], str(e))

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(generate_chunk, (i, chunk)): chunk
                   for i, chunk in enumerate(to_generate, 1)}
        for future in as_completed(futures):
            result = future.result()
            if result:
                errors.append(result)

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(generate_chunk, (i, chunk)): chunk
                   for i, chunk in enumerate(to_generate, 1)}
        for future in as_completed(futures):
            result = future.result()
            if result:
                errors.append(result)

    # Summary
    print(f"\nDone: {len(to_generate) - len(errors)} generated, {len(errors)} errors")
    if errors:
        print("\nFailed chunks:")
        for chunk_id, msg in errors:
            print(f"  {chunk_id}: {msg}")


if __name__ == "__main__":
    main()
