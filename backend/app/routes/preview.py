"""
Preview endpoint for the workout session audio generator backend.
Returns a Vietnamese workout script based on an uploaded CSV file_id.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from backend.app.schemas import PreviewRequest, PreviewResponse
from backend.app.services import preview_workout

router = APIRouter(tags=["preview"])


@router.post("/preview", response_model=PreviewResponse)
async def preview(request: PreviewRequest) -> PreviewResponse:
    """Preview the workout script for an uploaded CSV.

    Given a ``file_id``, loads the CSV and builds a Vietnamese
    preview script. Returns the script text and total exercise count.
    """
    try:
        script, total_exercises = preview_workout(request.file_id)
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"CSV file not found for file_id: {request.file_id}",
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    return PreviewResponse(
        file_id=request.file_id,
        script=script,
        total_exercises=total_exercises,
    )