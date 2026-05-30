"""
Download endpoint for the workout session audio generator backend.
Serves generated MP3 files for download.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from backend.app.services import get_output_path

router = APIRouter(tags=["download"])


@router.get("/download/{file_id}")
async def download_audio(file_id: str) -> FileResponse:
    """Download a generated workout audio MP3 file.

    Given a ``file_id``, returns the MP3 file from
    ``storage/outputs/{file_id}.mp3``.

    Raises HTTP 404 if the file does not exist.
    """
    try:
        output_path = get_output_path(file_id)
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Output file not found for file_id: {file_id}",
        )

    return FileResponse(
        path=str(output_path),
        media_type="audio/mpeg",
        filename=f"workout_{file_id}.mp3",
    )