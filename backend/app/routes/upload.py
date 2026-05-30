"""
CSV upload endpoint for the workout session audio generator backend.
"""

from __future__ import annotations

from uuid import uuid4

from fastapi import APIRouter, HTTPException, UploadFile

from backend.app.config import UPLOAD_DIR, ensure_directories
from backend.app.schemas import UploadResponse

router = APIRouter(tags=["upload"])


@router.post("/upload-csv", response_model=UploadResponse)
async def upload_csv(file: UploadFile) -> UploadResponse:
    """Upload a workout CSV file.

    Accepts a multipart form field named "file".
    Only ``.csv`` files are accepted.
    The file is saved to ``storage/uploads/{file_id}.csv``.
    """
    # Validate file type
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail=f"Only CSV files are accepted. Got: {file.filename}",
        )

    # Ensure storage directories exist
    ensure_directories()

    # Create a unique file_id and save path
    file_id = str(uuid4())
    stored_path = UPLOAD_DIR / f"{file_id}.csv"

    # Write the uploaded file to disk
    content = await file.read()
    stored_path.write_bytes(content)

    return UploadResponse(
        file_id=file_id,
        filename=file.filename,
        stored_path=str(stored_path),
    )