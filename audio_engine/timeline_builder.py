"""
Timeline builder for workout session audio generator.
Builds a timeline of voice and silence items from workout rows for
realistic work/rest workout audio.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from audio_engine.csv_loader import WorkoutRow, load_workout_csv


@dataclass
class TimelineItem:
    """
    A single item in the workout audio timeline.

    Attributes
    ----------
    type : str
        The type of timeline item: "voice" or "silence".
    text : str | None
        The text to speak (only for "voice" items).
    duration_seconds : int | None
        Duration in seconds (only for "silence" items).
    silence_kind : str | None
        Kind of silence: "work" for work periods, "rest" for rest periods.
        Only meaningful when type == "silence".
    """

    type: str  # "voice" or "silence"
    text: str | None = None
    duration_seconds: int | None = None
    silence_kind: str | None = None


def build_workout_timeline(exercises: list[WorkoutRow]) -> list[TimelineItem]:
    """
    Build a timeline of voice and silence items from workout exercises.

    The timeline structure for each day/session group:
      1. Voice: "[Buổi: <day>]" (if new day)
      2. Voice: "[Bài tập: <session>]" (if new session)
      3. For each exercise:
         a. Voice: introduce exercise name
         b. Voice: technical note (if note exists)
         c. For each set (1 to N):
            - Voice: "Chuẩn bị set X của <exercise>"
            - Voice: "Ba, hai, một, bắt đầu."
            - Silence: work_seconds (user works out), silence_kind="work"
            - Voice: "Nghỉ."
            - Silence: rest_seconds (user rests), silence_kind="rest"
                       — skip for last set of exercise
      4. After all exercises in a day/session:
         Voice: "Hoàn thành buổi tập!"

    Parameters
    ----------
    exercises : list[WorkoutRow]
        List of validated workout rows, ordered as they appear.

    Returns
    -------
    list[TimelineItem]
        Ordered list of timeline items.
    """
    timeline: list[TimelineItem] = []
    current_day: str | None = None
    current_session: str | None = None
    is_last_exercise = False

    for idx, row in enumerate(exercises):
        is_last_exercise = idx == len(exercises) - 1

        # Day header
        if row.day != current_day:
            timeline.append(
                TimelineItem(type="voice", text=f"Buổi {row.day}")
            )
            current_day = row.day
            current_session = None

        # Session header
        if row.session != current_session:
            timeline.append(
                TimelineItem(
                    type="voice",
                    text=f"Bài tập: {row.session}",
                )
            )
            current_session = row.session

        # Exercise introduction
        timeline.append(
            TimelineItem(
                type="voice",
                text=f"{row.exercise}",
            )
        )

        # Technical note
        note = row.note.strip()
        if note:
            timeline.append(
                TimelineItem(
                    type="voice",
                    text=f"Lưu ý: {note}",
                )
            )

        # Parse sets count
        try:
            num_sets = int(row.sets)
        except ValueError:
            num_sets = 1

        # Generate per-set items
        for set_num in range(1, num_sets + 1):
            is_last_set = set_num == num_sets

            # Prepare set
            timeline.append(
                TimelineItem(
                    type="voice",
                    text=f"Chuẩn bị set {set_num} của {row.exercise}.",
                )
            )

            # Countdown
            timeline.append(
                TimelineItem(
                    type="voice",
                    text="Ba, hai, một, bắt đầu.",
                )
            )

            # Work period (silence_kind="work")
            timeline.append(
                TimelineItem(
                    type="silence",
                    duration_seconds=row.work_seconds,
                    silence_kind="work",
                )
            )

            # Rest voice
            timeline.append(
                TimelineItem(
                    type="voice",
                    text="Nghỉ.",
                )
            )

            # Rest silence (silence_kind="rest") — skip for last set of the exercise
            if not is_last_set:
                timeline.append(
                    TimelineItem(
                        type="silence",
                        duration_seconds=row.rest_seconds,
                        silence_kind="rest",
                    )
                )

        # After exercise, if it's the last exercise, add completion
        if is_last_exercise:
            timeline.append(
                TimelineItem(
                    type="voice",
                    text="Hoàn thành buổi tập!",
                )
            )
        else:
            # Rest between exercises (silence_kind="rest")
            timeline.append(
                TimelineItem(
                    type="silence",
                    duration_seconds=row.rest_seconds,
                    silence_kind="rest",
                )
            )

    return timeline


def build_workout_timeline_from_csv(csv_path: Path) -> list[TimelineItem]:
    """
    Convenience function: load CSV and build timeline in one call.

    Parameters
    ----------
    csv_path : Path
        Path to the workout CSV file.

    Returns
    -------
    list[TimelineItem]
        Ordered list of timeline items.
    """
    rows = load_workout_csv(csv_path)
    return build_workout_timeline(rows)