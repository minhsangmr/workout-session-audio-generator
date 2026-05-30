"""
Exporter for workout session audio generator.
Concatenates voice MP3 segments into a single output MP3 file.
"""

from __future__ import annotations

from pathlib import Path

from pydub import AudioSegment


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