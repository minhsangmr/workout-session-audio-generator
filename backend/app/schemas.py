"""
Pydantic schemas for the workout session audio generator backend API.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class PreviewRequest(BaseModel):
    """Request schema for the /preview endpoint."""

    file_id: str = Field(..., description="UUID of the uploaded CSV file")


class GenerateAudioRequest(BaseModel):
    """Request schema for the /generate-audio endpoint."""

    file_id: str = Field(..., description="UUID of the uploaded CSV file")
    tts_engine: str = Field(default="gtts", description="TTS engine to use")
    timeline_mode: bool = Field(default=True, description="Use timeline mode")
    beep: bool = Field(default=False, description="Enable beep cues")
    background_music: str | None = Field(
        default=None, description="Path to background music file"
    )
    work_beep_offsets: list[int] = Field(
        default_factory=lambda: [5, 2],
        description="Beep offsets from end for work periods (seconds)",
    )
    rest_beep_offsets: list[int] = Field(
        default_factory=lambda: [5, 2],
        description="Beep offsets from end for rest periods (seconds)",
    )
    voice_music_volume_db: int = Field(
        default=-24, description="Background music volume during voice (dB)"
    )
    active_music_volume_db: int = Field(
        default=-12, description="Background music volume during silence (dB)"
    )
    fade_in_ms: int = Field(default=1000, description="Fade-in duration (ms)")
    fade_out_ms: int = Field(default=1500, description="Fade-out duration (ms)")


class UploadResponse(BaseModel):
    """Response schema for the /upload-csv endpoint."""

    file_id: str
    filename: str
    stored_path: str


class PreviewResponse(BaseModel):
    """Response schema for the /preview endpoint."""

    file_id: str
    script: str
    total_exercises: int


class GenerateAudioResponse(BaseModel):
    """Response schema for the /generate-audio endpoint."""

    file_id: str
    output_file: str
    download_url: str


class ErrorResponse(BaseModel):
    """Standard error response."""

    detail: str