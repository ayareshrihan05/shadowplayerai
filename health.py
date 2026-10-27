"""
health.py — System health and status check endpoint.
"""
from __future__ import annotations

import os
from fastapi import APIRouter
from api.dependencies import api_response
from database.db import is_seeded

router = APIRouter()


@router.get("/health")
def health_check():
    """Return system operational status, AI fallback status, and database connectivity."""
    ai_fallback = os.getenv("AI_FALLBACK_MODE", "true").lower() in ("true", "1", "yes")
    db_connected = is_seeded()

    return api_response({
        "status": "healthy",
        "version": "1.0.0",
        "database_connected": db_connected,
        "ai_fallback_mode": ai_fallback,
        "environment": "development",
        "message": "ShadowPlayer AI backend running. All data is synthetic.",
    })
