"""
Exporter for workout session audio generator.
Concatenates voice MP3 segments into a single output MP3 file.
Also supports exporting a full timeline (voice + silence) to MP3
with optional beep cues and background music.
"""

from __future__ import annotations

from pathlib import Path

from pydub import AudioSegment

from audio_engine.beep_builder import overlay_beeps_on_segment, overlay_beeps_on_silence
from audio_engine.music_mixer import apply_fade, load_background_music, loop_audio_to_duration
from audio_engine.timeline_builder import TimelineItem
from audio_engine.tts_generator import generate_tts_audio


def export_voice_segments_to_mp3(
    segment_paths: list[Path],
    output_path: Path,
    gap_ms: int = 500,
) -> Path:
    """
    Concatenate voice MP3 segments into a single MP3 file.

    Each segment is appended in order with a silence gap in between.

    Parameters
    ----------
    segment_paths : list[Path]
        Ordered list of paths to the voice MP3 segment files.
    output_path : Path
        Destination path for the combined MP3 file.
    gap_ms : int, optional
        Milliseconds of silence to insert between segments (default: 500).

    Returns
    -------
    Path
        The output_path of the combined MP3 file.

    Raises
    ------
    ValueError
        If segment_paths is empty.
    FileNotFoundError
        If any segment file does not exist.
    """
    if not segment_paths:
        raise ValueError(
            "segment_paths must contain at least one segment path."
        )

    silence_gap = AudioSegment.silent(duration=gap_ms)

    combined: AudioSegment | None = None

    for seg_path in segment_paths:
        if not seg_path.exists():
            raise FileNotFoundError(
                f"Voice segment file not found: {seg_path}"
            )

        segment_audio = AudioSegment.from_mp3(str(seg_path))

        if combined is None:
            combined = segment_audio
        else:
            combined += silence_gap + segment_audio

    # combined should never be None because we validate segment_paths is non-empty
    assert combined is not None

    # Ensure parent directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    combined.export(str(output_path), format="mp3")

    return output_path


def _get_item_duration_ms(item: TimelineItem) -> int:
    """Get the duration in ms of a single timeline item."""
    if item.type == "voice":
        return 0  # voice duration is unknown until TTS generates it
    if item.type == "silence" and item.duration_seconds is not None:
        return int(item.duration_seconds * 1000)
    return 0


def export_timeline_to_mp3(
    timeline: list[TimelineItem],
    output_path: Path,
    temp_dir: Path,
    language: str = "vi",
    tts_engine: str = "gtts",
    enable_beep: bool = False,
    work_beep_offsets: list[int] | None = None,
    rest_beep_offsets: list[int] | None = None,
    background_music_path: Path | None = None,
    voice_music_volume_db: int = -24,
    active_music_volume_db: int = -12,
    fade_in_ms: int = 1000,
    fade_out_ms: int = 1500,
) -> Path:
    """
    Export a workout timeline to a single MP3 file.

    Iterates through timeline items in order:
      - "voice" items: generate TTS audio and append.
      - "silence" items: append silent AudioSegment for the specified duration,
        optionally with beep cues overlaid if enable_beep is True.

    When ``background_music_path`` is provided, background music is looped
    across the entire timeline. Voice segments are overlaid onto quieter music
    (``voice_music_volume_db``) and silence/active segments use louder music
    (``active_music_volume_db``). Fade in/out is applied to the final mix.

    Parameters
    ----------
    timeline : list[TimelineItem]
        Ordered list of timeline items (voice/silence).
    output_path : Path
        Destination path for the final MP3 file.
    temp_dir : Path
        Temporary directory for intermediate TTS MP3 files.
    language : str, optional
        Language code for TTS (default: 'vi').
    tts_engine : str, optional
        TTS engine to use (default: 'gtts'). Only 'gtts' is supported in this MVP.
    enable_beep : bool, optional
        Whether to overlay beep cues on silence periods (default: False).
    work_beep_offsets : list[int] | None, optional
        Offsets from end in seconds for beeps during work periods.
        Default: [5, 2] (beep at 5s and 2s before end).
    rest_beep_offsets : list[int] | None, optional
        Offsets from end in seconds for beeps during rest periods.
        Default: [5, 2] (beep at 5s and 2s before end).
    background_music_path : Path | None, optional
        Path to background music file. If provided, music is mixed into
        the timeline (default: None).
    voice_music_volume_db : int, optional
        Volume reduction in dB for background music during voice segments
        (default: -24).
    active_music_volume_db : int, optional
        Volume reduction in dB for background music during silence/active
        segments (default: -12).
    fade_in_ms : int, optional
        Fade-in duration in ms for the final mix (default: 1000).
    fade_out_ms : int, optional
        Fade-out duration in ms for the final mix (default: 1500).

    Returns
    -------
    Path
        The output_path of the generated MP3 file.

    Raises
    ------
    ValueError
        If timeline is empty.
    RuntimeError
        If TTS generation fails.
    """
    if not timeline:
        raise ValueError("Timeline must contain at least one item.")

    if tts_engine != "gtts":
        raise ValueError(
            f"Only gtts is supported in this MVP. Got: {tts_engine}"
        )

    # Default beep offsets
    if work_beep_offsets is None:
        work_beep_offsets = [5, 2]
    if rest_beep_offsets is None:
        rest_beep_offsets = [5, 2]

    # Clean temp dir and recreate
    if temp_dir.exists():
        for f in temp_dir.iterdir():
            if f.is_file():
                f.unlink()
    temp_dir.mkdir(parents=True, exist_ok=True)

    tld = "com.vn" if language == "vi" else "com"

    # --- Load background music if requested ----------------------------------
    has_music = background_music_path is not None

    if has_music:
        try:
            background_music = load_background_music(background_music_path)  # type: ignore[arg-type]
        except (FileNotFoundError, ValueError) as exc:
            raise RuntimeError(f"Failed to load background music: {exc}") from exc
        music_duration_ms = len(background_music)
    else:
        background_music = None
        music_duration_ms = 0

    combined: AudioSegment | None = None
    voice_counter = 0
    current_position_ms = 0  # tracks position for slicing background music

    def _music_slice(start_ms: int, length_ms: int) -> AudioSegment:
        """Get a slice of background music, looping if necessary."""
        nonlocal background_music, music_duration_ms
        assert background_music is not None
        if music_duration_ms <= 0:
            return AudioSegment.silent(duration=length_ms)

        # Offset within the original music loop
        offset = start_ms % music_duration_ms
        # Build a looped version long enough to cover offset + length
        needed = offset + length_ms
        looped = loop_audio_to_duration(background_music, needed)
        return looped[offset:offset + length_ms]

    for item_idx, item in enumerate(timeline):
        if item.type == "voice":
            if not item.text:
                continue  # skip empty voice items

            voice_counter += 1
            voice_path = temp_dir / f"timeline_voice_{voice_counter:04d}.mp3"

            # Generate TTS for this voice item
            try:
                generate_tts_audio(
                    text=item.text,
                    output_path=voice_path,
                    lang=language,
                    tld=tld,
                )
            except RuntimeError as exc:
                raise RuntimeError(
                    f"Failed to generate TTS for timeline item {item_idx} "
                    f"(text: '{item.text[:50]}...'): {exc}"
                ) from exc

            segment_audio = AudioSegment.from_mp3(str(voice_path))
            segment_length = len(segment_audio)

            if has_music and background_music is not None:
                # Slice background music for this segment (with looping)
                music_slice = _music_slice(current_position_ms, segment_length)
                music_slice = music_slice.apply_gain(voice_music_volume_db)

                # Overlay voice onto quiet music
                mix_segment = music_slice.overlay(segment_audio)
            else:
                mix_segment = segment_audio

            if combined is None:
                combined = mix_segment
            else:
                combined += mix_segment

            current_position_ms += segment_length

        elif item.type == "silence":
            if item.duration_seconds is None:
                continue  # skip silence items with no duration

            silence_ms = int(item.duration_seconds * 1000)

            if has_music and background_music is not None:
                # Slice background music for this silence period (with looping)
                music_slice = _music_slice(current_position_ms, silence_ms)
                music_slice = music_slice.apply_gain(active_music_volume_db)

                if enable_beep and item.silence_kind:
                    if item.silence_kind == "work":
                        active_segment = overlay_beeps_on_segment(
                            base_segment=music_slice,
                            beep_offsets_from_end=work_beep_offsets,
                        )
                    elif item.silence_kind == "rest":
                        active_segment = overlay_beeps_on_segment(
                            base_segment=music_slice,
                            beep_offsets_from_end=rest_beep_offsets,
                        )
                    else:
                        active_segment = music_slice
                else:
                    active_segment = music_slice
            else:
                # No background music: use silence (with optional beep)
                if enable_beep and item.silence_kind:
                    if item.silence_kind == "work":
                        active_segment = overlay_beeps_on_silence(
                            duration_seconds=item.duration_seconds,
                            beep_offsets_from_end=work_beep_offsets,
                        )
                    elif item.silence_kind == "rest":
                        active_segment = overlay_beeps_on_silence(
                            duration_seconds=item.duration_seconds,
                            beep_offsets_from_end=rest_beep_offsets,
                        )
                    else:
                        active_segment = AudioSegment.silent(duration=silence_ms)
                else:
                    active_segment = AudioSegment.silent(duration=silence_ms)

            if combined is None:
                combined = active_segment
            else:
                combined += active_segment

            current_position_ms += silence_ms

    if combined is None:
        raise RuntimeError(
            "Failed to generate any audio from the timeline."
        )

    # Apply fade in/out on final mix if background music was used
    if has_music:
        combined = apply_fade(
            audio=combined,
            fade_in_ms=fade_in_ms,
            fade_out_ms=fade_out_ms,
        )

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Export final MP3
    combined.export(str(output_path), format="mp3")

    return output_path