"""
CLI entry point for workout session audio generator.

Usage:
    uv run python cli/generate.py --input <csv_path> [options]

Examples:
    # Preview mode
    uv run python cli/generate.py --input data/sample_inputs/sample_workout.csv --preview-only

    # MVP 3: Simple concatenation (default)
    uv run python cli/generate.py --input data/sample_inputs/sample_workout.csv --tts-engine gtts
    uv run python cli/generate.py --input data/sample_inputs/sample_workout.csv --tts-engine gtts --gap-ms 800

    # MVP 4: Timeline mode (work/rest periods)
    uv run python cli/generate.py --input data/sample_inputs/sample_workout.csv --tts-engine gtts --output storage/outputs/workout_timeline.mp3 --timeline-mode

    # MVP 5: Timeline mode with beep cues
    uv run python cli/generate.py --input data/sample_inputs/sample_workout.csv --tts-engine gtts --output storage/outputs/workout_beep.mp3 --timeline-mode --beep
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from audio_engine.csv_loader import load_workout_csv
from audio_engine.exporter import (
    export_timeline_to_mp3,
    export_voice_segments_to_mp3,
)
from audio_engine.script_builder import build_script
from audio_engine.timeline_builder import build_workout_timeline
from audio_engine.tts_generator import (
    generate_tts_segments,
    split_script_into_segments,
)


def _parse_beep_offsets(value: str) -> list[int]:
    """Parse a comma-separated string of integers into a list."""
    parts = value.split(",")
    offsets: list[int] = []
    for p in parts:
        stripped = p.strip()
        if stripped:
            try:
                offsets.append(int(stripped))
            except ValueError:
                raise argparse.ArgumentTypeError(
                    f"Invalid beep offset value: '{stripped}'. "
                    "Expected comma-separated integers, e.g. '5,2'."
                )
    return offsets


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
        help="Milliseconds of silence between voice segments (default: 500). "
        "Only used in non-timeline (MVP 3) mode.",
    )

    parser.add_argument(
        "--temp-dir",
        type=str,
        default="storage/temp",
        help="Temporary directory for voice segments (default: storage/temp).",
    )

    parser.add_argument(
        "--timeline-mode",
        action="store_true",
        help="Use timeline mode with work/rest periods (MVP 4). "
        "Builds a full workout timeline with voice and silence items.",
    )

    parser.add_argument(
        "--beep",
        action="store_true",
        help="Enable beep cues during work/rest silence periods "
        "(only in --timeline-mode). Beeps play at configurable offsets "
        "before the end of each period (default: 5s and 2s).",
    )

    parser.add_argument(
        "--work-beep-offsets",
        type=str,
        default="5,2",
        help="Comma-separated offsets in seconds from end of work periods "
        "for beep cues (default: '5,2'). Only used with --beep.",
    )

    parser.add_argument(
        "--rest-beep-offsets",
        type=str,
        default="5,2",
        help="Comma-separated offsets in seconds from end of rest periods "
        "for beep cues (default: '5,2'). Only used with --beep.",
    )

    # --- Background music options (MVP 6) ------------------------------------
    parser.add_argument(
        "--background-music",
        type=str,
        default=None,
        help="Path to background music MP3 file. Only used with --timeline-mode.",
    )

    parser.add_argument(
        "--voice-music-volume-db",
        type=int,
        default=-24,
        help="Volume reduction in dB for background music during voice "
        "segments (default: -24). Only used with --background-music.",
    )

    parser.add_argument(
        "--active-music-volume-db",
        type=int,
        default=-12,
        help="Volume reduction in dB for background music during work/rest "
        "silence periods (default: -12). Only used with --background-music.",
    )

    parser.add_argument(
        "--fade-in-ms",
        type=int,
        default=1000,
        help="Fade-in duration in milliseconds for final mix "
        "(default: 1000). Only used with --background-music.",
    )

    parser.add_argument(
        "--fade-out-ms",
        type=int,
        default=1500,
        help="Fade-out duration in milliseconds for final mix "
        "(default: 1500). Only used with --background-music.",
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

    # Validate TTS engine
    if args.tts_engine != "gtts":
        print(
            f"Error: Only gtts is supported in this MVP. Got: {args.tts_engine}",
            file=sys.stderr,
        )
        sys.exit(1)

    temp_dir = Path(args.temp_dir)
    output_path = Path(args.output)

    # --- Background music warning --------------------------------------------
    if args.background_music and not args.timeline_mode:
        print(
            "Warning: --background-music is only supported in --timeline-mode. "
            "Ignoring background music.",
            file=sys.stderr,
        )
        args.background_music = None

    # --- Timeline mode (MVP 4 & 5) --------------------------------------------
    if args.timeline_mode:
        # 1. Load CSV
        try:
            rows = load_workout_csv(csv_path)
        except (FileNotFoundError, ValueError) as exc:
            print(f"Error loading CSV: {exc}", file=sys.stderr)
            sys.exit(1)

        # 2. Build timeline
        print("Building workout timeline...")
        timeline = build_workout_timeline(rows)

        # Parse beep offsets if --beep is enabled
        work_beep_offsets = _parse_beep_offsets(args.work_beep_offsets)
        rest_beep_offsets = _parse_beep_offsets(args.rest_beep_offsets)

        print(
            f"Timeline has {len(timeline)} items "
            f"({sum(1 for t in timeline if t.type == 'voice')} voice, "
            f"{sum(1 for t in timeline if t.type == 'silence')} silence)."
        )

        if args.beep:
            print(
                f"Beep cues enabled: work offsets {work_beep_offsets}s, "
                f"rest offsets {rest_beep_offsets}s"
            )

        if args.background_music:
            print(
                f"Background music enabled: {args.background_music} "
                f"(voice vol: {args.voice_music_volume_db} dB, "
                f"active vol: {args.active_music_volume_db} dB)"
            )

        # 3. Export timeline to MP3
        print(f"Generating timeline audio via gTTS to {output_path}...")
        try:
            result_path = export_timeline_to_mp3(
                timeline=timeline,
                output_path=output_path,
                temp_dir=temp_dir,
                enable_beep=args.beep,
                work_beep_offsets=work_beep_offsets,
                rest_beep_offsets=rest_beep_offsets,
                background_music_path=Path(args.background_music) if args.background_music else None,
                voice_music_volume_db=args.voice_music_volume_db,
                active_music_volume_db=args.active_music_volume_db,
                fade_in_ms=args.fade_in_ms,
                fade_out_ms=args.fade_out_ms,
            )
        except (ValueError, RuntimeError) as exc:
            print(f"Error exporting timeline audio: {exc}", file=sys.stderr)
            sys.exit(1)

        print(f"\nGenerated timeline workout audio:\n{result_path}")
        return

    # --- Non-timeline mode (MVP 3: simple concatenation) --------------------
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