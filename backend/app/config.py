"""
Configuration for the workout session audio generator backend.
Uses pathlib for cross-platform path management.
"""

from __future__ import annotations

from pathlib import Path


# Project root: backend/
ROOT_DIR = Path(__file__).resolve().parent.parent

# Storage directories
STORAGE_DIR = ROOT_DIR.parent / "storage"
UPLOAD_DIR = STORAGE_DIR / "uploads"
OUTPUT_DIR = STORAGE_DIR / "outputs"
TEMP_DIR = STORAGE_DIR / "temp"


def ensure_directories() -> None:
    """Create required storage directories if they don't exist."""
    for directory in (UPLOAD_DIR, OUTPUT_DIR, TEMP_DIR):
        directory.mkdir(parents=True, exist_ok=True)