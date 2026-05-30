"""
Audio generation endpoint for the workout session audio generator backend.
Generates workout MP3 audio based on an uploaded CSV file_id and options.
"""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException

from backend.app.schemas import GenerateAudioRequest, GenerateAudioResponse
from backend.app.services import generate_audio

router = APIRouter(tags=["generate"])


@router.post("/generate-audio", response_model=GenerateAudioResponse)
async def generate(request: GenerateAudioRequest) -> GenerateAudioResponse:
    """Generate workout audio MP3 from an uploaded CSV.

    Accepts a JSON body with ``file_id`` and audio generation options.
    The output MP3 is saved to ``storage/outputs/{file_id}.mp3``.
    Returns the output path and a download URL.
    """
    try:
        output_path = generate_audio(
            file_id=request.file_id,
            tts_engine=request.tts_engine,
            timeline_mode=request.timeline_mode,
            enable_beep=request.beep,
            background_music=request.background_music,
            work_beep_offsets=request.work_beep_offsets,
            rest_beep_offsets=request.rest_beep_offsets,
            voice_music_volume_db=request.voice_music_volume_db,
            active_music_volume_db=request.active_music_volume_db,
            fade_in_ms=request.fade_in_ms,
            fade_out_ms=request.fade_out_ms,
        )
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    return GenerateAudioResponse(
        file_id=request.file_id,
        output_file=str(output_path),
        download_url=f"/download/{request.file_id}",
    )