# Workout Session Audio Generator

Generate MP3 workout audio from a CSV workout plan using TTS (Text-to-Speech).

## Features

- **CSV Loader** — Reads and validates workout CSV files.
- **Script Builder** — Builds a Vietnamese preview script from workout data.
- **TTS Generator** — Generates MP3 voice segments using gTTS (Vietnamese).
- **Simple Export (MVP 3)** — Concatenates voice segments into a single MP3 with configurable gaps.
- **Timeline Export (MVP 4)** — Full workout timeline with voice cues and real work/rest silence periods.

## Quick Start

```bash
# Preview script
uv run python cli/generate.py --input data/sample_inputs/sample_workout.csv --preview-only

# Simple concatenation (MVP 3)
uv run python cli/generate.py --input data/sample_inputs/sample_workout.csv --tts-engine gtts

# Timeline mode with work/rest periods (MVP 4)
uv run python cli/generate.py --input data/sample_inputs/sample_workout.csv --tts-engine gtts --timeline-mode

# Custom output / gap
uv run python cli/generate.py --input data/sample_inputs/sample_workout.csv --tts-engine gtts --output storage/outputs/my_workout.mp3 --gap-ms 800
```

## Usage

```
uv run python cli/generate.py --input <csv_path> [options]

Options:
  --input PATH          Path to workout CSV (required)
  --preview-only        Print script only, no audio
  --tts-engine ENGINE   TTS engine (default: gtts)
  --output PATH         Output MP3 path (default: storage/outputs/workout.mp3)
  --gap-ms MS           Silence gap between segments, MVP 3 only (default: 500)
  --temp-dir PATH       Temp directory for voice files (default: storage/temp)
  --timeline-mode       Full timeline with work/rest periods (MVP 4)
```

## Timeline Mode (MVP 4)

When `--timeline-mode` is enabled, the generator builds a structured workout audio with:

1. Voice intro for each day/session
2. Voice exercise introduction
3. Per-set voice cues:
   - "Chuẩn bị set X..."
   - "Ba, hai, một, bắt đầu."
   - Work silence (work_seconds)
   - "Nghỉ."
   - Rest silence (rest_seconds)
4. Voice completion at the end

## Project Structure

```
audio_engine/
├── csv_loader.py         # CSV parsing & validation
├── script_builder.py     # Vietnamese script generation
├── tts_generator.py      # gTTS voice generation
├── timeline_builder.py   # Workout timeline construction
└── exporter.py           # MP3 concatenation & timeline export

cli/
└── generate.py           # CLI entry point

data/
└── sample_inputs/        # Sample CSV workout files

storage/
├── outputs/              # Generated MP3 files
└── temp/                 # Temporary voice segments
```

## Requirements

- Python >= 3.12
- See `pyproject.toml` for dependencies.