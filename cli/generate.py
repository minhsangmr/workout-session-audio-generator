"""
CLI entry point for workout audio generation.
Supports preview-only mode to display workout scripts in terminal.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from audio_engine.csv_loader import load_workout_csv
from audio_engine.script_builder import build_preview_script


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse and return CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Workout Session Audio Generator — CLI preview tool"
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
    else:
        print("Audio generation is not implemented yet.")


if __name__ == "__main__":
    main()