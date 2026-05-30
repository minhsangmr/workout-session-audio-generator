"""
Music mixer for workout session audio generator.
Provides utilities for loading background music, looping to a target duration,
applying fade in/out, and mixing music with voice/beep segments.
"""

from __future__ import annotations

from pathlib import Path

from pydub import AudioSegment


def load_background_music(music_path: Path) -> AudioSegment:
    """
    Load a background music file and convert to stereo.

    Parameters
    ----------
    music_path : Path
        Path to the background music MP3 (or other audio) file.

    Returns
    -------
    AudioSegment
        The loaded audio, converted to stereo.

    Raises
    ------
    FileNotFoundError
        If the music file does not exist.
    ValueError
        If the file cannot be decoded as audio.
    """
    if not music_path.exists():
        raise FileNotFoundError(f"Background music file not found: {music_path}")

    try:
        audio = AudioSegment.from_file(str(music_path))
    except Exception as exc:
        raise ValueError(
            f"Failed to decode audio file '{music_path}': {exc}"
        ) from exc

    # Convert to stereo if mono
    if audio.channels == 1:
        audio = audio.set_channels(2)

    return audio


def loop_audio_to_duration(
    audio: AudioSegment,
    target_duration_ms: int,
) -> AudioSegment:
    """
    Loop or trim audio to exactly match the target duration.

    Parameters
    ----------
    audio : AudioSegment
        The source audio segment to loop or trim.
    target_duration_ms : int
        Desired total duration in milliseconds. Must be > 0.

    Returns
    -------
    AudioSegment
        The resulting audio with exactly target_duration_ms length.

    Raises
    ------
    ValueError
        If target_duration_ms <= 0.
    """
    if target_duration_ms <= 0:
        raise ValueError(
            f"target_duration_ms must be > 0, got {target_duration_ms}"
        )

    audio_duration = len(audio)

    if audio_duration <= 0:
        raise ValueError("Audio segment has zero or negative duration.")

    if audio_duration >= target_duration_ms:
        # Trim to target duration
        return audio[:target_duration_ms]

    # Loop until we reach or exceed target duration
    repeats = (target_duration_ms // audio_duration) + 1
    looped = audio * repeats

    # Trim to exact target duration
    return looped[:target_duration_ms]


def apply_fade(
    audio: AudioSegment,
    fade_in_ms: int = 1000,
    fade_out_ms: int = 1500,
) -> AudioSegment:
    """
    Apply fade-in and fade-out to an audio segment.

    Durations are automatically clamped to half the audio length so they
    never exceed sensible bounds.

    Parameters
    ----------
    audio : AudioSegment
        The audio to apply fading to.
    fade_in_ms : int, optional
        Fade-in duration in milliseconds (default: 1000).
    fade_out_ms : int, optional
        Fade-out duration in milliseconds (default: 1500).

    Returns
    -------
    AudioSegment
        The audio with fade applied.
    """
    total_ms = len(audio)

    # Clamp fade durations to reasonable values
    max_fade = total_ms // 2
    fade_in_ms = min(fade_in_ms, max_fade) if fade_in_ms > 0 else 0
    fade_out_ms = min(fade_out_ms, max_fade) if fade_out_ms > 0 else 0

    result = audio

    if fade_in_ms > 0:
        result = result.fade_in(fade_in_ms)

    if fade_out_ms > 0:
        result = result.fade_out(fade_out_ms)

    return result