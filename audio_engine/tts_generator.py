"""
TTS generator for workout session audio.
Splits script into segments and generates MP3 files using gTTS.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import List

from gtts import gTTS


def split_script_into_segments(script: str) -> List[str]:
    """Split a workout script into meaningful text segments for TTS generation.

    Each non-empty line becomes a segment. Lines that are purely separators
    (dashes, equals, or box-drawing characters) are dropped.

    Args:
        script: The full workout script text.

    Returns:
        List of text segments, each suitable for TTS conversion.
    """
    segments: List[str] = []
    separator_pattern = re.compile(r"^[\s═─➜•✔✗━—=+\-|]+$")

    for line in script.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        # Skip purely decorative/separator lines
        if separator_pattern.match(stripped):
            continue
        # Skip very short meaningless fragments (e.g. empty bullet)
        if len(stripped) < 3:
            continue
        segments.append(stripped)

    return segments


def generate_tts_segments(
    texts: List[str],
    output_dir: Path,
    language: str = "vi",
) -> List[Path]:
    """Generate TTS audio files for each text segment using gTTS.

    Creates output_dir if it does not exist. Clears any existing
    voice_*.mp3 files in the directory before generating new ones.

    Args:
        texts: List of text strings to convert to speech.
        output_dir: Directory to write MP3 files into.
        language: Language code for gTTS (default "vi").

    Returns:
        List of Paths to the generated MP3 files.

    Raises:
        RuntimeError: If gTTS fails to generate audio for a segment.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Remove old voice_*.mp3 files to avoid stale segments
    for old_file in output_dir.glob("voice_*.mp3"):
        old_file.unlink()

    generated: List[Path] = []

    for idx, text in enumerate(texts, start=1):
        filename = f"voice_{idx:03d}.mp3"
        filepath = output_dir / filename

        try:
            tts = gTTS(text=text, lang=language, slow=False)
            tts.save(str(filepath))
        except Exception as e:
            raise RuntimeError(
                f"Failed to generate TTS for segment {idx} (text: {text[:60]!r}...): {e}"
            )

        if not filepath.exists() or filepath.stat().st_size == 0:
            raise RuntimeError(
                f"TTS output file is empty or missing for segment {idx}: {filepath}"
            )

        generated.append(filepath)

    return generated