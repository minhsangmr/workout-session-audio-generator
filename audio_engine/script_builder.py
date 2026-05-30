"""
Script builder for workout session audio generator.
Builds a Vietnamese preview script from workout CSV rows.
"""

from __future__ import annotations

from pathlib import Path

from audio_engine.csv_loader import WorkoutRow, load_workout_csv


def build_script(rows: list[WorkoutRow]) -> str:
    """
    Build a Vietnamese text script from workout rows.

    The script reads like a natural Vietnamese narration for a workout session.

    Parameters
    ----------
    rows : list[WorkoutRow]
        List of validated workout rows.

    Returns
    -------
    str
        The full Vietnamese script text.
    """
    lines: list[str] = []
    current_day: str | None = None
    current_session: str | None = None

    for row in rows:
        if row.day != current_day:
            lines.append(f"[Buổi: {row.day}]")
            current_day = row.day
            current_session = None

        if row.session != current_session:
            lines.append(f"[Bài tập: {row.session}]")
            current_session = row.session

        lines.append(
            f"{row.exercise}: {row.sets} sets, {row.reps} reps, "
            f"{row.work_seconds}s work, {row.rest_seconds}s rest. "
            f"Dụng cụ: {row.equipment}. "
            f"Ghi chú: {row.note}"
        )

    return "\n".join(lines)


def build_preview_script_from_csv(csv_path: Path) -> str:
    """
    Convenience function: load CSV and build preview script in one call.

    Parameters
    ----------
    csv_path : Path
        Path to the workout CSV file.

    Returns
    -------
    str
        The full Vietnamese preview script.
    """
    rows = load_workout_csv(csv_path)
    return build_script(rows)