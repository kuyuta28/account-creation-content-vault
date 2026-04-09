#!/usr/bin/env python3
"""
gen_clips.py — Combine TTS audio + AI images into video clips using ffmpeg.

Usage:
    python gen_clips.py --project <path>           # generate all missing clips
    python gen_clips.py --project <path> --dry-run  # show what would be generated
    python gen_clips.py --project <path> --force    # regenerate even existing clips
    python gen_clips.py --project <path> --clip 00-01  # single clip

Each clip:
  - Audio: assets/audio/audio-XX-YY.mp3
  - Images: assets/images/IMG-XX-YY_1.png, IMG-XX-YY_2.png, ...
  - Output: assets/clips/clip-XX-YY.mp4

If there are 2 image variants, the clip crossfades from variant 1 → variant 2
at the midpoint of the audio. If only 1 image variant, it's shown static.
"""

import argparse
import asyncio
import json
import re
import subprocess
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def parse_audio_image_map(script_dir: Path) -> list[dict]:
    """
    Parse audio-image-map.md.
    Returns list of {audio_id, image_id} where IDs are like "00-01".

    Expected format:
        | # | Audio     | Image |
        |---|-----------|-------|
        | 1 | 00-01.mp3 | 00-01 |
    """
    map_file = script_dir / "audio-image-map.md"
    if not map_file.exists():
        raise FileNotFoundError(f"audio-image-map.md not found in {script_dir}")

    rows: list[dict] = []
    row_pattern = re.compile(r"^\|\s*\d+\s*\|\s*(\S+)\s*\|\s*(\S+)\s*\|")

    for line in map_file.read_text(encoding="utf-8").splitlines():
        m = row_pattern.match(line)
        if not m:
            continue
        audio_file = m.group(1).strip()   # "00-01.mp3" or "audio-00-01.mp3"
        image_id   = m.group(2).strip()   # "00-01"

        # Normalise audio ID
        audio_stem = audio_file.removesuffix(".mp3")
        if not audio_stem.startswith("audio-"):
            audio_stem = f"audio-{audio_stem}"

        rows.append({"audio_id": audio_stem, "image_id": image_id})

    if not rows:
        raise ValueError(f"No rows parsed from {map_file}")
    return rows


def find_image_variants(images_dir: Path, image_id: str) -> list[Path]:
    """Return sorted list of image variant files: IMG-XX-YY_1.png, IMG-XX-YY_2.png …"""
    prefix = f"IMG-{image_id}_"
    variants = sorted(images_dir.glob(f"{prefix}*.png"))
    return variants


# ---------------------------------------------------------------------------
# ffmpeg helpers
# ---------------------------------------------------------------------------

def get_audio_duration(audio_path: Path) -> float:
    """Return audio duration in seconds using ffprobe."""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "json",
        str(audio_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)
    return float(data["format"]["duration"])


def build_static_clip(audio: Path, image: Path, output: Path) -> None:
    """Create clip: static image + audio."""
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(image),
        "-i", str(audio),
        "-c:v", "libx264", "-tune", "stillimage",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest",
        str(output),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed:\n{result.stderr[-1000:]}")


def build_crossfade_clip(
    audio: Path, img1: Path, img2: Path, output: Path, xfade_duration: float = 1.0
) -> None:
    """
    Create clip: img1 → crossfade → img2, with audio.
    Crossfade starts at audio_duration/2 - xfade_duration/2.
    """
    duration = get_audio_duration(audio)
    # Time offset where xfade starts (halfway through audio minus half xfade)
    xfade_offset = max(0.0, duration / 2 - xfade_duration / 2)

    # Each image segment padded to cover the full duration
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-t", str(duration), "-i", str(img1),
        "-loop", "1", "-t", str(duration), "-i", str(img2),
        "-i", str(audio),
        "-filter_complex",
        f"[0:v][1:v]xfade=transition=fade:duration={xfade_duration}:offset={xfade_offset}[v]",
        "-map", "[v]",
        "-map", "2:a",
        "-c:v", "libx264", "-tune", "stillimage",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-t", str(duration),
        str(output),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed:\n{result.stderr[-1000:]}")


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def build_clip(audio_dir: Path, images_dir: Path, clips_dir: Path, row: dict) -> Path:
    """Build a single clip. Returns output path. Raises on error."""
    audio_id = row["audio_id"]   # "audio-00-01"
    image_id = row["image_id"]   # "00-01"

    audio = audio_dir / f"{audio_id}.mp3"
    if not audio.exists():
        raise FileNotFoundError(f"Audio not found: {audio}")

    variants = find_image_variants(images_dir, image_id)
    if not variants:
        raise FileNotFoundError(f"No images found for image_id={image_id} in {images_dir}")

    # clip-00-01.mp4
    clip_suffix = image_id  # same XX-YY format
    output = clips_dir / f"clip-{clip_suffix}.mp4"
    clips_dir.mkdir(parents=True, exist_ok=True)

    if len(variants) >= 2:
        build_crossfade_clip(audio, variants[0], variants[1], output)
    else:
        build_static_clip(audio, variants[0], output)

    return output


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate video clips from audio + images")
    parser.add_argument("--project", required=True, help="Path to project dir")
    parser.add_argument("--dry-run", action="store_true", help="Show plan without generating")
    parser.add_argument("--force", action="store_true", help="Regenerate existing clips")
    parser.add_argument("--clip", help="Generate specific clip ID only (e.g. 00-01)")
    args = parser.parse_args()

    project_dir = Path(args.project).expanduser().resolve()
    if not project_dir.exists():
        print(f"ERROR: project dir not found: {project_dir}", file=sys.stderr)
        sys.exit(1)

    script_dir = project_dir / "script"
    audio_dir  = project_dir / "assets" / "audio"
    images_dir = project_dir / "assets" / "images"
    clips_dir  = project_dir / "assets" / "clips"

    rows = parse_audio_image_map(script_dir)

    # Filter by --clip if specified
    if args.clip:
        rows = [r for r in rows if r["image_id"] == args.clip]
        if not rows:
            print(f"ERROR: clip ID '{args.clip}' not found in audio-image-map.md", file=sys.stderr)
            sys.exit(1)

    # Determine which clips need to be built
    pending: list[dict] = []
    for row in rows:
        output = clips_dir / f"clip-{row['image_id']}.mp4"
        if output.exists() and not args.force:
            print(f"  skip  clip-{row['image_id']}.mp4 (exists)")
        else:
            pending.append(row)

    if not pending:
        print("All clips already exist. Use --force to regenerate.")
        return

    if args.dry_run:
        print(f"\nWould generate {len(pending)} clip(s):")
        for row in pending:
            variants = find_image_variants(images_dir, row["image_id"])
            mode = "crossfade" if len(variants) >= 2 else "static"
            print(f"  clip-{row['image_id']}.mp4  [{mode}, {len(variants)} image variant(s)]")
        return

    print(f"\nGenerating {len(pending)} clip(s)...")
    errors: list[tuple[str, str]] = []

    for i, row in enumerate(pending, 1):
        clip_name = f"clip-{row['image_id']}.mp4"
        print(f"  [{i}/{len(pending)}] {clip_name} ...", end=" ", flush=True)
        try:
            output = build_clip(audio_dir, images_dir, clips_dir, row)
            size_mb = output.stat().st_size / 1_048_576
            print(f"done ({size_mb:.1f} MB)")
        except Exception as e:
            print(f"FAILED: {e}")
            errors.append((clip_name, str(e)))

    print(f"\n{'─'*60}")
    print(f"Done.  Generated={len(pending) - len(errors)}  Errors={len(errors)}")
    if errors:
        print("\nFailed clips:")
        for name, msg in errors:
            print(f"  {name}: {msg}")
        sys.exit(1)


if __name__ == "__main__":
    main()
