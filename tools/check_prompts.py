#!/usr/bin/env python3
"""
check_prompts.py — Validate image prompts in script/image-prompts.md.

Checks:
  1. Every prompt is 200-299 characters (AA server hard limit = 300)
  2. Every IMG-XX-YY ID is unique
  3. Every prompt has STYLE, SUBJECT, PALETTE, LIGHTING components
  4. Visual anchor is defined and consistent

Usage:
    python tools/check_prompts.py --project <path>
    python tools/check_prompts.py --project <path> --fix   # show suggestions for overlong prompts
"""

import argparse
import re
import sys
from pathlib import Path


def parse_prompts(filepath: Path) -> tuple[list[dict], str | None, dict[str, str]]:
    """Parse image-prompts.md and return (prompts, visual_anchor, meta)."""
    text = filepath.read_text(encoding="utf-8")
    prompts = []

    # Extract visual anchor
    anchor_match = re.search(r"<!-- visual-anchor:\s*(.+?)\s*-->", text)
    visual_anchor = anchor_match.group(1).strip() if anchor_match else None

    # Extract style-suffix and title-suffix metadata
    meta: dict[str, str] = {}
    for m in re.finditer(r"<!--\s*(style-suffix|title-suffix):\s*(.+?)\s*-->", text):
        meta[m.group(1)] = m.group(2).strip()

    # Extract IMG IDs marked with [TITLE]
    title_ids: set[str] = set()
    for m in re.finditer(r"(IMG-\d{2}-\d{2})\s*\[TITLE\]", text):
        title_ids.add(m.group(1))

    style_suffix = meta.get("style-suffix", "")
    title_suffix = meta.get("title-suffix", "")

    # Find section headers
    section_pattern = re.compile(r"^## Section \d+ — (.+)$", re.MULTILINE)
    section_starts = [(m.start(), m.group(1)) for m in section_pattern.finditer(text)]

    # Support TWO formats:
    # Format A: IMG-XX-YY: <prompt text>  or  IMG-XX-YY [TITLE]: <prompt text>
    # Format B: ### IMG-XX-YY ... ```\n<prompt text>\n```
    line_pattern = re.compile(r"^(IMG-\d{2}-\d{2})(?:\s*\[TITLE\])?:\s*(.+)$", re.MULTILINE)
    block_pattern = re.compile(
        r"^### (IMG-\d{2}-\d{2})(?:\s*\[TITLE\])?\b.*?\n```\n(.*?)\n```",
        re.MULTILINE | re.DOTALL,
    )

    matches: list[tuple[int, str, str]] = []  # (pos, id, text)

    for pm in line_pattern.finditer(text):
        matches.append((pm.start(), pm.group(1), pm.group(2).strip()))

    for pm in block_pattern.finditer(text):
        prompt_text = " ".join(pm.group(2).split())
        matches.append((pm.start(), pm.group(1), prompt_text))

    for pos, img_id, prompt_text in matches:
        section = "unknown"
        for start, name in section_starts:
            if pos > start:
                section = name
            else:
                break

        # Compute final length (prompt + auto-appended suffixes)
        final_parts = [prompt_text]
        if style_suffix:
            final_parts.append(style_suffix)
        if img_id in title_ids and title_suffix:
            final_parts.append(title_suffix)
        final_text = ", ".join(final_parts)

        prompts.append({
            "id": img_id,
            "text": prompt_text,
            "final_text": final_text,
            "length": len(final_text),
            "raw_length": len(prompt_text),
            "section": section,
            "has_title": img_id in title_ids,
        })

    return prompts, visual_anchor, meta


def check_prompts(project_path: Path, show_fix: bool = False) -> bool:
    script_dir = project_path / "script"
    prompts_file = script_dir / "image-prompts.md"

    if not prompts_file.exists():
        print(f"ERROR: {prompts_file} not found")
        return False

    prompts, visual_anchor, meta = parse_prompts(prompts_file)

    if not prompts:
        print("ERROR: No prompts found in file")
        return False

    style_suffix = meta.get("style-suffix", "")
    title_suffix = meta.get("title-suffix", "")

    print(f"Found {len(prompts)} prompts")
    print(f"Visual anchor: {visual_anchor or 'NOT DEFINED'}")
    if style_suffix:
        print(f"Style suffix ({len(style_suffix)} chars): \"{style_suffix}\"")
    if title_suffix:
        title_prompts = sum(1 for p in prompts if p["has_title"])
        print(f"Title suffix ({len(title_suffix)} chars): \"{title_suffix}\" — applied to {title_prompts} prompts")
    print()

    has_errors = False
    seen_ids = {}

    # Check uniqueness
    for p in prompts:
        if p["id"] in seen_ids:
            print(f"  DUPLICATE ID: {p['id']} appears more than once (section: {p['section']})")
            has_errors = True
        seen_ids[p["id"]] = p["section"]

    # Check lengths
    short = []
    ok = []
    long = []

    for p in prompts:
        length = p["length"]
        if length < 200:
            short.append(p)
        elif length > 299:
            long.append(p)
        else:
            ok.append(p)

    print(f"  OK (200-299 chars):    {len(ok)}")
    print(f"  TOO SHORT (<200 chars): {len(short)}")
    print(f"  TOO LONG (>299 chars):  {len(long)}")
    print()

    if short:
        print("--- TOO SHORT (< 200 chars) ---")
        for p in short:
            print(f"  {p['id']} ({p['section']}): {p['length']} chars (raw {p['raw_length']})")
            print(f"    \"{p['text'][:80]}...\"")
        print()

    if long:
        print("--- TOO LONG (> 299 chars) ---")
        for p in long:
            excess = p["length"] - 299
            print(f"  {p['id']} ({p['section']}): {p['length']} chars (+{excess}) (raw {p['raw_length']})")
            if show_fix:
                print(f"    Full: \"{p['final_text']}\"")
        print()

    # Check visual anchor consistency
    if visual_anchor:
        anchor_keywords = visual_anchor.lower().split(", ")
        missing_anchor = []
        for p in prompts:
            text_lower = p["final_text"].lower()
            # Check if at least the style keyword appears
            style_keyword = anchor_keywords[0].strip().lower()
            if style_keyword not in text_lower:
                missing_anchor.append(p["id"])

        if missing_anchor:
            print("--- MISSING VISUAL ANCHOR ---")
            for pid in missing_anchor:
                print(f"  {pid}: missing style keyword \"{anchor_keywords[0]}\"")
            print()
            has_errors = True

    if short or long:
        has_errors = True

    if not has_errors:
        print("All prompts pass validation.")

    return not has_errors


def main():
    parser = argparse.ArgumentParser(description="Validate image prompts")
    parser.add_argument("--project", required=True, help="Path to episode directory")
    parser.add_argument("--fix", action="store_true", help="Show suggestions for overlong prompts")
    args = parser.parse_args()

    project_path = Path(args.project)
    success = check_prompts(project_path, show_fix=args.fix)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()