"""
Beep builder for workout session audio generator.
Generates beep AudioSegment and overlays beeps onto silence periods.
"""

from __future__ import annotations

from pydub import AudioSegment
from pydub.generators import Sine


def create_beep(
    duration_ms: int = 300,
    frequency_hz: int = 880,
    volume_db: int = -6,
) -> AudioSegment:
    """
    Create a short beep (sine wave) AudioSegment.

    Parameters
    ----------
    duration_ms : int, optional
        Duration of the beep in milliseconds (default: 300).
    frequency_hz : int, optional
        Frequency of the beep in Hz (default: 880, approximately A5).
    volume_db : int, optional
        Volume adjustment in dB relative to the generated sine (default: -6).

    Returns
    -------
    AudioSegment
        The beep AudioSegment ready to overlay or play.
    """
    beep = Sine(frequency_hz).to_audio_segment(duration=duration_ms)
    beep = beep.apply_gain(volume_db)
    return beep


def overlay_beeps_on_silence(
    duration_seconds: int,
    beep_offsets_from_end: list[int],
    frequency_hz: int = 880,
    beep_duration_ms: int = 300,
) -> AudioSegment:
    """
    Create a silent AudioSegment with beeps overlaid at specific offsets
    from the end of the silence.

    Parameters
    ----------
    duration_seconds : int
        Total duration of the silence in seconds.
    beep_offsets_from_end : list[int]
        List of offsets in seconds from the end at which to place beeps.
        For example, [5, 2] means beeps at (end - 5s) and (end - 2s).
        Offsets larger than duration or <= 0 are ignored.
    frequency_hz : int, optional
        Frequency of each beep in Hz (default: 880).
    beep_duration_ms : int, optional
        Duration of each beep in milliseconds (default: 300).

    Returns
    -------
    AudioSegment
        The silence AudioSegment with beeps overlaid at the specified positions.
    """
    duration_ms = duration_seconds * 1000
    silence = AudioSegment.silent(duration=duration_ms)

    beep = create_beep(
        duration_ms=beep_duration_ms,
        frequency_hz=frequency_hz,
    )

    for offset_sec in beep_offsets_from_end:
        if offset_sec <= 0:
            continue
        if offset_sec > duration_seconds:
            continue

        # Calculate position in ms from start
        position_ms = duration_ms - (offset_sec * 1000 + beep_duration_ms)

        # Ensure non-negative position
        if position_ms < 0:
            position_ms = 0

        silence = silence.overlay(beep, position=position_ms)

    return silence