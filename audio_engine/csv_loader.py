"""
CSV loader for workout session audio generator.
Reads and validates workout CSV input files.
"""

from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

import pandas as pd


class WorkoutRow(NamedTuple):
    """A single row from the workout CSV."""

    day: str
    session: str
    exercise: str
    sets: str
    reps: str
    work_seconds: int
    rest_seconds: int
    equipment: str
    note: str


def load_workout_csv(csv_path: Path) -> list[WorkoutRow]:
    """
    Load and validate a workout CSV file.

    Parameters
    ----------
    csv_path : Path
        Path to the CSV file.

    Returns
    -------
    list[WorkoutRow]
        List of validated workout rows.

    Raises
    ------
    FileNotFoundError
        If the CSV file does not exist.
    ValueError
        If the CSV is missing required columns or has invalid data.
    """
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    required_columns = {
        "day",
        "session",
        "exercise",
        "sets",
        "reps",
        "work_seconds",
        "rest_seconds",
        "equipment",
        "note",
    }

    df = pd.read_csv(csv_path)

    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(
            f"CSV is missing required columns: {', '.join(sorted(missing))}. "
            f"File: {csv_path}"
        )

    rows: list[WorkoutRow] = []
    for idx, row in df.iterrows():
        try:
            work_sec = int(row["work_seconds"])
            rest_sec = int(row["rest_seconds"])
        except (ValueError, TypeError) as exc:
            raise ValueError(
                f"Invalid numeric value at row {idx + 2} "
                f"(0-indexed: {idx}): {exc}"
            ) from exc

        rows.append(
            WorkoutRow(
                day=str(row["day"]),
                session=str(row["session"]),
                exercise=str(row["exercise"]),
                sets=str(row["sets"]),
                reps=str(row["reps"]),
                work_seconds=work_sec,
                rest_seconds=rest_sec,
                equipment=str(row["equipment"]),
                note=str(row["note"]),
            )
        )

    if not rows:
        raise ValueError(f"CSV file is empty (no data rows): {csv_path}")

    return rows