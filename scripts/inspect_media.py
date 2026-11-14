#!/usr/bin/env python3
"""Inventory video, audio, and image files with FFprobe.

Usage:
    python scripts/inspect_media.py <file-or-folder> [--json output.json]

Requires ffprobe on PATH. The script is read-only.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


MEDIA_EXTENSIONS = {
    ".mp4", ".mov", ".m4v", ".webm", ".mkv", ".avi",
    ".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg",
    ".png", ".jpg", ".jpeg", ".webp", ".gif", ".tif", ".tiff",
}


def probe(path: Path) -> dict:
    command = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration,size,format_name:stream=index,codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels",
        "-of", "json", str(path),
    ]
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    result = json.loads(completed.stdout)
    result["path"] = str(path.resolve())
    return result


def collect(target: Path) -> list[Path]:
    if target.is_file():
        return [target]
    if not target.is_dir():
        raise FileNotFoundError(target)
    return sorted(
        path for path in target.rglob("*")
        if path.is_file() and path.suffix.lower() in MEDIA_EXTENSIONS
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path)
    parser.add_argument("--json", dest="json_path", type=Path)
    args = parser.parse_args()

    if not shutil.which("ffprobe"):
        print("ERROR: ffprobe was not found on PATH.", file=sys.stderr)
        return 2

    try:
        files = collect(args.target)
    except FileNotFoundError:
        print(f"ERROR: target not found: {args.target}", file=sys.stderr)
        return 2

    records = []
    for path in files:
        try:
            records.append(probe(path))
        except subprocess.CalledProcessError as exc:
            records.append({"path": str(path.resolve()), "error": exc.stderr.strip()})

    output = json.dumps(records, ensure_ascii=False, indent=2)
    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(output + "\n", encoding="utf-8")
        print(f"Wrote {len(records)} records to {args.json_path}")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


