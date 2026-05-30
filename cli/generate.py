"""
CLI entry point for workout session audio generator.

Usage:
    uv run python cli/generate.py --input <csv_path> [options]

Examples:
    # Preview mode
    uv run python cli/generate.py --input data/sample_inputs/sample_workout.csv --preview-only

    # Generate full MP3 with default gap
    uv run python cli/generate.py --input data/sample_inputs/sample_workout.csv --tts-engine gtts

    # Generate full MP3 with custom gap
    uv run python cli/generate.py --input data/sample_inputs/sample_workout.csv --tts-engine gtts --gap-ms 800

    # Generate with custom output path
    uv run python cli/generate.py --input data/sample_inputs/sample_workout.csv --tts-engine gtts --output storage/outputs/workout.mp3
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from audio_engine.csv_loader import load_workout_csv
from audio_engine.exporter import export_voice_segments_to_mp3
from audio_engine.script_builder import build_script
from audio_engine.tts_generator import (
    generate_tts_segments,
    split_script_into_segments,
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate workout session audio from a CSV workout plan."
    )

    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to the workout CSV file.",
    )

    parser.add_argument(
        "--preview-only",
        action="store_true",
        help="Only print the preview script without generating audio.",
    )

    parser.add_argument(
        "--tts-engine",
        type=str,
        default="gtts",
        choices=["gtts"],
        help="TTS engine to use (default: gtts).",
    )

    parser.add_argument(
        "--output",
        type=str,
        default="storage/outputs/workout.mp3",
        help="Output path for the final MP3 file (default: storage/outputs/workout.mp3).",
    )

    parser.add_argument(
        "--gap-ms",
        type=int,
        default=500,
        help="Milliseconds of silence between voice segments (default: 500).",
    )

    parser.add_argument(
        "--temp-dir",
        type=str,
        default="storage/temp",
        help="Temporary directory for voice segments (default: storage/temp).",
    )

    return parser


def main() -> None:
    """Main CLI entry point."""
    parser = _build_parser()
    args = parser.parse_args()

    csv_path = Path(args.input)

    # --- Preview mode --------------------------------------------------------
    if args.preview_only:
        try:
            rows = load_workout_csv(csv_path)
        except (FileNotFoundError, ValueError) as exc:
            print(f"Error loading CSV: {exc}", file=sys.stderr)
            sys.exit(1)

        script = build_script(rows)
        print(script)
        return

    # --- Full generation mode ------------------------------------------------
    # Validate TTS engine
    if args.tts_engine != "gtts":
        print(
            f"Error: Only gtts is supported in this MVP. Got: {args.tts_engine}",
            file=sys.stderr,
        )
        sys.exit(1)

    temp_dir = Path(args.temp_dir)
    output_path = Path(args.output)
    gap_ms = args.gap_ms

    if gap_ms < 0:
        print(
            f"Error: gap_ms must be non-negative, got {gap_ms}.",
            file=sys.stderr,
        )
        sys.exit(1)

    # 1. Load CSV
    try:
        rows = load_workout_csv(csv_path)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error loading CSV: {exc}", file=sys.stderr)
        sys.exit(1)

    # 2. Build script
    script = build_script(rows)

    # 3. Split into segments
    segments = split_script_into_segments(script)

    if not segments:
        print("Error: No text segments to generate audio from.", file=sys.stderr)
        sys.exit(1)

    # 4. Generate TTS segments
    print(f"Generating {len(segments)} voice segments via gTTS...")
    try:
        segment_paths = generate_tts_segments(
            segments=segments,
            temp_dir=temp_dir,
        )
    except RuntimeError as exc:
        print(f"Error generating TTS: {exc}", file=sys.stderr)
        sys.exit(1)

    # 5. Export combined MP3
    print(f"Concatenating {len(segment_paths)} segments into {output_path}...")
    try:
        result_path = export_voice_segments_to_mp3(
            segment_paths=segment_paths,
            output_path=output_path,
            gap_ms=gap_ms,
        )
    except (ValueError, FileNotFoundError) as exc:
        print(f"Error exporting audio: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"\nGenerated final workout audio:\n{result_path}")


if __name__ == "__main__":
    main()