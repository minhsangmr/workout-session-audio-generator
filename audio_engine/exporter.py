"""
Exporter for workout session audio generator.
Concatenates voice MP3 segments into a single output MP3 file.
Also supports exporting a full timeline (voice + silence) to MP3.
"""

from __future__ import annotations

from pathlib import Path

from pydub import AudioSegment

from audio_engine.beep_builder import overlay_beeps_on_silence
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


def export_timeline_to_mp3(
    timeline: list[TimelineItem],
    output_path: Path,
    temp_dir: Path,
    language: str = "vi",
    tts_engine: str = "gtts",
    enable_beep: bool = False,
    work_beep_offsets: list[int] | None = None,
    rest_beep_offsets: list[int] | None = None,
) -> Path:
    """
    Export a workout timeline to a single MP3 file.

    Iterates through timeline items in order:
      - "voice" items: generate TTS audio and append.
      - "silence" items: append silent AudioSegment for the specified duration,
        optionally with beep cues overlaid if enable_beep is True.

    Temp files are created in temp_dir and cleaned up after export.

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

    combined: AudioSegment | None = None
    voice_counter = 0

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

            if combined is None:
                combined = segment_audio
            else:
                combined += segment_audio

        elif item.type == "silence":
            if item.duration_seconds is None:
                continue  # skip silence items with no duration

            silence_ms = item.duration_seconds * 1000

            if enable_beep and item.silence_kind:
                # Overlay beeps on silence based on silence_kind
                if item.silence_kind == "work":
                    silence_segment = overlay_beeps_on_silence(
                        duration_seconds=item.duration_seconds,
                        beep_offsets_from_end=work_beep_offsets,
                    )
                elif item.silence_kind == "rest":
                    silence_segment = overlay_beeps_on_silence(
                        duration_seconds=item.duration_seconds,
                        beep_offsets_from_end=rest_beep_offsets,
                    )
                else:
                    # Unknown silence_kind, just plain silence
                    silence_segment = AudioSegment.silent(duration=silence_ms)
            else:
                silence_segment = AudioSegment.silent(duration=silence_ms)

            if combined is None:
                combined = silence_segment
            else:
                combined += silence_segment

    if combined is None:
        raise RuntimeError(
            "Failed to generate any audio from the timeline."
        )

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Export final MP3
    combined.export(str(output_path), format="mp3")

    return output_path