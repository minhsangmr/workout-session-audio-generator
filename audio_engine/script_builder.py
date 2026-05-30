"""
Script builder for workout sessions.
Generates a human-readable Vietnamese workout script from Exercise data.
"""

from __future__ import annotations

from collections import OrderedDict
from typing import Dict, List

from audio_engine.csv_loader import Exercise


def _format_seconds(seconds: int) -> str:
    """Convert seconds to a readable format like '50 giây' or '1 phút 30 giây'."""
    if seconds < 60:
        return f"{seconds} giây"
    minutes = seconds // 60
    secs = seconds % 60
    if secs == 0:
        return f"{minutes} phút"
    return f"{minutes} phút {secs} giây"


def _group_by_day_session(exercises: List[Exercise]) -> Dict[str, Dict[str, List[Exercise]]]:
    """Group exercises by day, then by session, preserving insertion order."""
    grouped: Dict[str, Dict[str, List[Exercise]]] = OrderedDict()
    for ex in exercises:
        if ex.day not in grouped:
            grouped[ex.day] = OrderedDict()
        if ex.session not in grouped[ex.day]:
            grouped[ex.day][ex.session] = []
        grouped[ex.day][ex.session].append(ex)
    return grouped


def build_preview_script(exercises: List[Exercise]) -> str:
    """Build a Vietnamese preview script from a list of Exercise objects.

    The script groups exercises by day/session and produces a readable
    workout plan with intro, exercise details, set simulation, and outro.

    Args:
        exercises: List of Exercise instances.

    Returns:
        A formatted Vietnamese workout script string.
    """
    if not exercises:
        return "Không có bài tập nào để hiển thị."

    grouped = _group_by_day_session(exercises)
    lines: List[str] = []

    total_days = len(grouped)
    total_exercises = len(exercises)

    # ── Intro ──
    lines.append("=" * 60)
    lines.append("  📋 LỊCH TẬP WORKOUT")
    lines.append("=" * 60)
    lines.append(f"  Tổng số buổi: {total_days}")
    lines.append(f"  Tổng số bài tập: {total_exercises}")
    lines.append("=" * 60)
    lines.append("")

    for day_idx, (day, sessions) in enumerate(grouped.items(), start=1):
        lines.append(f"{'─' * 50}")
        lines.append(f"  🗓  BUỔI {day_idx}: {day.upper()}")
        lines.append(f"{'─' * 50}")
        lines.append("")

        for session_idx, (session, session_exercises) in enumerate(sessions.items(), start=1):
            lines.append(f"  📌 Phần {session_idx}: {session}")
            lines.append("")

            for ex_idx, ex in enumerate(session_exercises, start=1):
                lines.append(f"    🔹 Bài {ex_idx}: {ex.exercise}")

                # Equipment
                eq = ex.equipment.strip()
                if eq and eq.lower() != "none" and eq != "-":
                    lines.append(f"       Dụng cụ: {eq}")

                # Reps & sets info
                lines.append(f"       Số set: {ex.sets}  |  Reps: {ex.reps}")

                # Work / Rest
                work_str = _format_seconds(ex.work_seconds)
                rest_str = _format_seconds(ex.rest_seconds)
                lines.append(f"       Work: {work_str}  |  Nghỉ: {rest_str}")

                # Note
                note = ex.note.strip()
                if note and note.lower() not in ("none", "-", ""):
                    lines.append(f"       Ghi chú: {note}")

                # Simulate each set briefly
                for s in range(1, ex.sets + 1):
                    lines.append(
                        f"         ➜ Set {s}/{ex.sets}: tập {work_str}, "
                        f"nghỉ {rest_str if s < ex.sets else '—'}"
                    )

                lines.append("")

        lines.append("")

    # ── Outro ──
    lines.append("=" * 60)
    lines.append("  ✅ HOÀN THÀNH BUỔI TẬP")
    lines.append("  Hãy nghỉ ngơi, uống đủ nước và giãn cơ sau khi tập!")
    lines.append("=" * 60)

    return "\n".join(lines)