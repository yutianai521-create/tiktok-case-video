#!/usr/bin/env python3
"""Validate structural properties of a rendered short-form video.

Usage:
    python scripts/validate_video.py video.mp4
    python scripts/validate_video.py video.mp4 --width 1080 --height 1920 --min-duration 12 --max-duration 25 --require-audio

Requires ffprobe on PATH. This does not replace visual review.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from fractions import Fraction
from pathlib import Path


def run_probe(path: Path) -> dict:
    command = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration:stream=codec_type,codec_name,width,height,r_frame_rate,duration",
        "-of", "json", str(path),
    ]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def fps(value: str | None) -> float | None:
    if not value or value == "0/0":
        return None
    return float(Fraction(value))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path)
    parser.add_argument("--width", type=int, default=1080)
    parser.add_argument("--height", type=int, default=1920)
    parser.add_argument("--min-duration", type=float, default=10.0)
    parser.add_argument("--max-duration", type=float, default=30.0)
    parser.add_argument("--min-fps", type=float, default=23.0)
    parser.add_argument("--require-audio", action="store_true")
    args = parser.parse_args()

    if not args.video.is_file():
        print(f"FAIL: video not found: {args.video}")
        return 2
    if not shutil.which("ffprobe"):
        print("FAIL: ffprobe was not found on PATH.")
        return 2

    try:
        data = run_probe(args.video)
    except (subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        print(f"FAIL: could not inspect video: {exc}")
        return 2

    streams = data.get("streams", [])
    videos = [stream for stream in streams if stream.get("codec_type") == "video"]
    audios = [stream for stream in streams if stream.get("codec_type") == "audio"]
    problems: list[str] = []

    if not videos:
        problems.append("no video stream")
    else:
        video = videos[0]
        if video.get("width") != args.width or video.get("height") != args.height:
            problems.append(
                f"canvas is {video.get('width')}x{video.get('height')}, expected {args.width}x{args.height}"
            )
        rate = fps(video.get("r_frame_rate"))
        if rate is None or rate < args.min_fps:
            problems.append(f"frame rate is {rate!r}, expected at least {args.min_fps}")

    duration_text = data.get("format", {}).get("duration")
    try:
        duration = float(duration_text)
    except (TypeError, ValueError):
        duration = None
        problems.append("duration could not be read")
    if duration is not None and not (args.min_duration <= duration <= args.max_duration):
        problems.append(
            f"duration is {duration:.3f}s, expected {args.min_duration:.3f}–{args.max_duration:.3f}s"
        )
    if args.require_audio and not audios:
        problems.append("audio stream is required but missing")

    if problems:
        print("FAIL")
        for problem in problems:
            print(f"- {problem}")
        return 1

    video = videos[0]
    print("PASS")
    print(f"- file: {args.video.resolve()}")
    print(f"- canvas: {video.get('width')}x{video.get('height')}")
    print(f"- duration: {duration:.3f}s")
    print(f"- fps: {fps(video.get('r_frame_rate')):.3f}")
    print(f"- video codec: {video.get('codec_name')}")
    print(f"- audio streams: {len(audios)}")
    print("- visual review is still required")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


