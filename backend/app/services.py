"""
Service layer for the workout session audio generator backend.
Wraps audio_engine functions for use by route handlers.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from audio_engine.csv_loader import load_workout_csv
from audio_engine.exporter import (
    export_timeline_to_mp3,
    export_voice_segments_to_mp3,
)
from audio_engine.script_builder import build_script
from audio_engine.timeline_builder import build_workout_timeline
from audio_engine.tts_generator import generate_tts_segments, split_script_into_segments

from backend.app.config import UPLOAD_DIR, OUTPUT_DIR, TEMP_DIR


def get_csv_path(file_id: str) -> Path:
    """Get the full path to an uploaded CSV file by its file_id.

    Parameters
    ----------
    file_id : str
        The UUID of the uploaded CSV.

    Returns
    -------
    Path
        The path to the CSV file.

    Raises
    ------
    FileNotFoundError
        If the CSV file does not exist.
    """
    csv_path = UPLOAD_DIR / f"{file_id}.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found for file_id: {file_id}")
    return csv_path


def load_csv(file_id: str) -> list[Any]:
    """Load workout CSV rows by file_id.

    Parameters
    ----------
    file_id : str
        The UUID of the uploaded CSV.

    Returns
    -------
    list[WorkoutRow]
        List of workout rows.
    """
    csv_path = get_csv_path(file_id)
    return load_workout_csv(csv_path)


def preview_workout(file_id: str) -> tuple[str, int]:
    """Build a preview script from an uploaded CSV.

    Parameters
    ----------
    file_id : str
        The UUID of the uploaded CSV.

    Returns
    -------
    tuple[str, int]
        (preview_script, total_exercises)
    """
    rows = load_csv(file_id)
    script = build_script(rows)
    total_exercises = len(rows)
    return script, total_exercises


def generate_audio(
    file_id: str,
    tts_engine: str = "gtts",
    timeline_mode: bool = True,
    enable_beep: bool = False,
    background_music: str | None = None,
    work_beep_offsets: list[int] | None = None,
    rest_beep_offsets: list[int] | None = None,
    voice_music_volume_db: int = -24,
    active_music_volume_db: int = -12,
    fade_in_ms: int = 1000,
    fade_out_ms: int = 1500,
) -> Path:
    """Generate workout audio MP3 from an uploaded CSV.

    Parameters
    ----------
    file_id : str
        The UUID of the uploaded CSV.
    tts_engine : str, optional
        TTS engine to use (default: 'gtts').
    timeline_mode : bool, optional
        Use timeline mode for realistic work/rest timing (default: True).
    enable_beep : bool, optional
        Enable beep cues during silence periods (default: False).
    background_music : str | None, optional
        Path to background music file (default: None).
    work_beep_offsets : list[int] | None, optional
        Beep offsets from end for work periods (default: [5, 2]).
    rest_beep_offsets : list[int] | None, optional
        Beep offsets from end for rest periods (default: [5, 2]).
    voice_music_volume_db : int, optional
        Background music volume during voice in dB (default: -24).
    active_music_volume_db : int, optional
        Background music volume during silence in dB (default: -12).
    fade_in_ms : int, optional
        Fade-in duration in ms (default: 1000).
    fade_out_ms : int, optional
        Fade-out duration in ms (default: 1500).

    Returns
    -------
    Path
        Path to the generated MP3 output file.
    """
    rows = load_csv(file_id)

    output_path = OUTPUT_DIR / f"{file_id}.mp3"
    temp_dir = TEMP_DIR / file_id

    if timeline_mode:
        # Build timeline and export with timeline exporter
        timeline = build_workout_timeline(rows)

        # Resolve background music path if provided
        music_path: Path | None = None
        if background_music:
            music_path = Path(background_music)
            if not music_path.exists():
                raise FileNotFoundError(
                    f"Background music file not found: {background_music}"
                )

        export_timeline_to_mp3(
            timeline=timeline,
            output_path=output_path,
            temp_dir=temp_dir,
            tts_engine=tts_engine,
            enable_beep=enable_beep,
            work_beep_offsets=work_beep_offsets,
            rest_beep_offsets=rest_beep_offsets,
            background_music_path=music_path,
            voice_music_volume_db=voice_music_volume_db,
            active_music_volume_db=active_music_volume_db,
            fade_in_ms=fade_in_ms,
            fade_out_ms=fade_out_ms,
        )
    else:
        # Non-timeline mode: script → segments → TTS → export
        script = build_script(rows)
        segments = split_script_into_segments(script)
        segment_paths = generate_tts_segments(segments, temp_dir=temp_dir)
        export_voice_segments_to_mp3(
            segment_paths=segment_paths,
            output_path=output_path,
        )

    return output_path


def get_output_path(file_id: str) -> Path:
    """Get the path to a generated output MP3 file.

    Parameters
    ----------
    file_id : str
        The UUID of the file.

    Returns
    -------
    Path
        The path to the output MP3 file.

    Raises
    ------
    FileNotFoundError
        If the output MP3 file does not exist.
    """
    output_path = OUTPUT_DIR / f"{file_id}.mp3"
    if not output_path.exists():
        raise FileNotFoundError(f"Output file not found for file_id: {file_id}")
    return output_path