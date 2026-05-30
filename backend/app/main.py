"""
FastAPI application entry point for the workout session audio generator backend.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routes.health import router as health_router
from backend.app.routes.upload import router as upload_router
from backend.app.routes.preview import router as preview_router
from backend.app.routes.generate import router as generate_router
from backend.app.routes.download import router as download_router

app = FastAPI(
    title="Workout Session Audio Generator API",
    description="Backend API for generating workout session audio files from CSV workout plans.",
    version="0.1.0",
)

# ---------------------------------------------------------------------------
# CORS Middleware
# Allow requests from local frontend origins.
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Include routers
# ---------------------------------------------------------------------------
app.include_router(health_router)
app.include_router(upload_router)
app.include_router(preview_router)
app.include_router(generate_router)
app.include_router(download_router)