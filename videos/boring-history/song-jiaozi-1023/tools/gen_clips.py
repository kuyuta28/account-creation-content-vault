"""
gen_clips.py — merge image + audio → .mp4 clip (duration = audio length)

Usage:
    python tools/gen_clips.py
    python tools/gen_clips.py --workers 4
    python tools/gen_clips.py --dry-run

Output: assets/clips/XX-XX.mp4

Prerequisites: ffmpeg must be on PATH
"""

import argparse
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent

AUDIO_DIR = PROJECT_DIR / "assets" / "audio"
IMAGE_DIR = PROJECT_DIR / "assets" / "images"
CLIPS_DIR = PROJECT_DIR / "assets" / "clips"

MAP_FILE = PROJECT_DIR / "script" / "audio-image-map.md"

DEFAULT_WORKERS = 4


def parse_map(map_file: Path) -> list[tuple[str, str]]:
    """Parse audio-image-map.md → list of (audio_stem, image_stem)."""
    pairs = []
    for line in map_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cols = [c.strip() for c in line.split("|")[1:-1]]
        if len(cols) < 3:
            continue
        if not cols[0].isdigit():
            continue
        audio_stem = cols[1].replace(".mp3", "")
        image_stem = cols[2]
        pairs.append((audio_stem, image_stem))
    return pairs


def build_clip(audio_stem: str, image_stem: str, dry_run: bool) -> tuple[str, str]:
    """Run ffmpeg to merge image + audio → clip. Returns (stem, status)."""
    audio_path = AUDIO_DIR / f"{audio_stem}.mp3"
    image_path = IMAGE_DIR / f"{image_stem}.png"
    out_path = CLIPS_DIR / f"{audio_stem}.mp4"

    if out_path.exists():
        return audio_stem, "skip"

    missing = []
    if not audio_path.exists():
        missing.append(str(audio_path))
    if not image_path.exists():
        missing.append(str(image_path))
    if missing:
        return audio_stem, f"MISSING: {', '.join(missing)}"

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", str(image_path),
        "-i", str(audio_path),
        "-shortest",
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        str(out_path),
    ]

    if dry_run:
        print(f"[dry-run] {' '.join(cmd)}")
        return audio_stem, "dry-run"

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return audio_stem, f"ERROR: {result.stderr[-300:]}"
    return audio_stem, "ok"


def main():
    parser = argparse.ArgumentParser(description="Merge images + audio into .mp4 clips")
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    CLIPS_DIR.mkdir(parents=True, exist_ok=True)

    pairs = parse_map(MAP_FILE)
    if not pairs:
        print("No pairs found in map file.")
        sys.exit(1)

    print(f"Found {len(pairs)} pairs. Workers: {args.workers}")

    results = {"ok": 0, "skip": 0, "error": 0, "dry-run": 0}
    errors = []

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(build_clip, audio, image, args.dry_run): audio
            for audio, image in pairs
        }
        for future in as_completed(futures):
            stem, status = future.result()
            if status == "ok":
                results["ok"] += 1
                print(f"  ✓ {stem}.mp4")
            elif status == "skip":
                results["skip"] += 1
                print(f"  - {stem}.mp4 (already exists)")
            elif status == "dry-run":
                results["dry-run"] += 1
            else:
                results["error"] += 1
                errors.append(f"{stem}: {status}")
                print(f"  ✗ {stem}: {status}")

    print(f"\nDone: {results['ok']} ok, {results['skip']} skipped, {results['error']} errors")
    if errors:
        print("\nErrors:")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
