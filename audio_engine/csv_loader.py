"""
CSV loader for workout session data.
Reads, validates, and parses workout CSV files into Exercise dataclass instances.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class Exercise:
    """Represents a single exercise entry from a workout CSV."""

    day: str
    session: str
    exercise: str
    sets: int
    reps: str
    work_seconds: int
    rest_seconds: int
    equipment: str
    note: str


REQUIRED_COLUMNS = [
    "day",
    "session",
    "exercise",
    "sets",
    "reps",
    "work_seconds",
    "rest_seconds",
    "equipment",
    "note",
]


def load_workout_csv(csv_path: Path) -> List[Exercise]:
    """Load and validate a workout CSV file, returning a list of Exercise objects.

    Args:
        csv_path: Path to the CSV file.

    Returns:
        List of parsed Exercise instances.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If the CSV is missing required columns or contains invalid data.
    """
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    with csv_path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        if reader.fieldnames is None:
            raise ValueError("CSV file is empty or has no header row.")

        # Validate required columns
        missing = [col for col in REQUIRED_COLUMNS if col not in reader.fieldnames]
        if missing:
            raise ValueError(
                f"Missing required column(s): {', '.join(missing)}\n"
                f"Expected columns: {', '.join(REQUIRED_COLUMNS)}"
            )

        exercises: List[Exercise] = []
        for row_num, row in enumerate(reader, start=2):  # row 1 = header
            # Check for empty values
            empty_cols = [
                col for col in REQUIRED_COLUMNS if not row.get(col, "").strip()
            ]
            if empty_cols:
                raise ValueError(
                    f"Row {row_num}: missing or empty value in column(s): {', '.join(empty_cols)}"
                )

            try:
                sets = int(row["sets"].strip())
            except ValueError:
                raise ValueError(
                    f"Row {row_num}, column 'sets': expected integer, got '{row['sets']}'"
                )

            try:
                work_seconds = int(row["work_seconds"].strip())
            except ValueError:
                raise ValueError(
                    f"Row {row_num}, column 'work_seconds': expected integer, got '{row['work_seconds']}'"
                )

            try:
                rest_seconds = int(row["rest_seconds"].strip())
            except ValueError:
                raise ValueError(
                    f"Row {row_num}, column 'rest_seconds': expected integer, got '{row['rest_seconds']}'"
                )

            exercises.append(
                Exercise(
                    day=row["day"].strip(),
                    session=row["session"].strip(),
                    exercise=row["exercise"].strip(),
                    sets=sets,
                    reps=row["reps"].strip(),
                    work_seconds=work_seconds,
                    rest_seconds=rest_seconds,
                    equipment=row["equipment"].strip(),
                    note=row["note"].strip(),
                )
            )

        return exercises