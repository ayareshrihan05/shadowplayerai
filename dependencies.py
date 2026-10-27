"""
dependencies.py — Shared FastAPI dependencies and response helpers.
All endpoints use the standard ShadowPlayer AI envelope format.
"""
from __future__ import annotations

import datetime
from typing import Any
from fastapi import HTTPException
from database.db import get_cache


def get_match_cache() -> dict:
    """Return the populated in-memory cache, or raise 503 if not ready."""
    cache = get_cache()
    if not cache or "matches" not in cache or not cache["matches"]:
        raise HTTPException(
            status_code=503,
            detail={"code": "DATABASE_NOT_READY", "message": "Match cache is empty or initialising"},
        )
    return cache


def api_response(data: Any, data_label: str = "SYNTHETIC DATA") -> dict:
    """Wrap response in standard JSON envelope."""
    return {
        "success": True,
        "data": data,
        "meta": {
            "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "data_label": data_label,
        },
    }


def api_error(code: str, message: str, status_code: int = 404) -> HTTPException:
    """Return formatted HTTP exception conforming to API contract."""
    return HTTPException(
        status_code=status_code,
        detail={
            "success": False,
            "error": {
                "code": code,
                "message": message,
            },
        },
    )
