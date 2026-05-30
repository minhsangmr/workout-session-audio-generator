"""
CLI entry point for workout audio generation.
Supports preview-only mode and TTS audio generation.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from audio_engine.csv_loader import load_workout_csv
from audio_engine.script_builder import build_preview_script
from audio_engine.tts_generator import generate_tts_segments, split_script_into_segments


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse and return CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Workout Session Audio Generator — CLI tool"
    )
    parser.add_argument(
        "--input",
        "-i",
        type=str,
        required=True,
        help="Path to the workout CSV file",
    )
    parser.add_argument(
        "--preview-only",
        action="store_true",
        help="Print the workout script to terminal instead of generating audio",
    )
    parser.add_argument(
        "--tts-engine",
        type=str,
        default=None,
        help="TTS engine to use (only 'gtts' is supported in this MVP)",
    )
    parser.add_argument(
        "--temp-dir",
        type=str,
        default="storage/temp",
        help="Directory to store temporary TTS audio files (default: storage/temp)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    """Main CLI entry point."""
    args = parse_args(argv)
    csv_path = Path(args.input)

    if args.preview_only:
        try:
            exercises = load_workout_csv(csv_path)
            script = build_preview_script(exercises)
            print(script)
        except (FileNotFoundError, ValueError) as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        return

    tts_engine = (args.tts_engine or "").lower()

    if tts_engine and tts_engine != "gtts":
        print(
            f"Error: Only gtts is supported in this MVP. Got '{args.tts_engine}'.",
            file=sys.stderr,
        )
        sys.exit(1)

    if not tts_engine:
        print("Audio generation is not implemented yet.")
        return

    # tts_engine == "gtts"
    try:
        exercises = load_workout_csv(csv_path)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    script = build_preview_script(exercises)
    segments = split_script_into_segments(script)

    temp_dir = Path(args.temp_dir)
    try:
        mp3_files = generate_tts_segments(segments, output_dir=temp_dir)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Generated {len(mp3_files)} MP3 files in: {temp_dir.resolve()}")
    for mp3_path in mp3_files:
        print(f"  - {mp3_path}")


if __name__ == "__main__":
    main()