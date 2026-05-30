"""
TTS generator for workout session audio generator.
Splits a script into segments and generates MP3 voice files using gTTS.
"""

from __future__ import annotations

from pathlib import Path

from gtts import gTTS


def split_script_into_segments(script: str) -> list[str]:
    """
    Split a full script text into individual segments (one per line).

    Empty lines and lines starting with '[' (markers) are kept as
    segments for timing context, but can also be spoken.

    Parameters
    ----------
    script : str
        The full script text.

    Returns
    -------
    list[str]
        List of text segments.
    """
    return [line.strip() for line in script.splitlines() if line.strip()]


def generate_tts_segments(
    segments: list[str],
    temp_dir: Path,
    lang: str = "vi",
    tld: str = "com.vn",
) -> list[Path]:
    """
    Generate MP3 voice segments from a list of text segments using gTTS.

    Each segment is saved as voice_001.mp3, voice_002.mp3, etc.

    Parameters
    ----------
    segments : list[str]
        List of text segments to convert to speech.
    temp_dir : Path
        Directory to save the generated MP3 files.
    lang : str, optional
        Language code for gTTS (default: 'vi').
    tld : str, optional
        Top-level domain for gTTS to localize accent (default: 'com.vn').

    Returns
    -------
    list[Path]
        List of paths to the generated MP3 files, in order.

    Raises
    ------
    RuntimeError
        If any segment fails to generate.
    """
    temp_dir.mkdir(parents=True, exist_ok=True)

    segment_paths: list[Path] = []

    for idx, text in enumerate(segments, start=1):
        output_path = temp_dir / f"voice_{idx:03d}.mp3"

        try:
            tts = gTTS(text=text, lang=lang, tld=tld, slow=False)
            tts.save(str(output_path))
        except Exception as exc:
            raise RuntimeError(
                f"Failed to generate TTS for segment {idx} "
                f"(text: '{text[:50]}...'): {exc}"
            ) from exc

        segment_paths.append(output_path)

    return segment_paths