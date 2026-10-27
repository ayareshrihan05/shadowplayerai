"""
reports.py — AI Scouting Report generation endpoint.
All data served is synthetic and fictional.
"""
from __future__ import annotations

from pydantic import BaseModel
from fastapi import APIRouter, Depends, Body
from api.dependencies import get_match_cache, api_response, api_error
from ai.narrative_service import generate_scouting_report

from ai.fallback_templates import generate_fallback_report

router = APIRouter()


class PlayerReportRequest(BaseModel):
    player_id: str
    match_id: str = "match-alpha-001"
    tier: str = "analyst"  # 'casual', 'analyst', 'coach'


@router.post("/reports/player")
def create_scouting_report(
    req: PlayerReportRequest = Body(...),
    cache: dict = Depends(get_match_cache),
):
    """
    Generate an AI scouting report explaining a player's off-ball contributions.
    Supports 3 tiers: casual, analyst, coach.
    Falls back deterministically if Microsoft Foundry AI is unreachable.
    """
    profile = cache["profiles"].get((req.player_id, req.match_id))
    if not profile:
        raise api_error("NOT_FOUND", f"Player '{req.player_id}' not found in match '{req.match_id}'")

    report_sections = generate_fallback_report(profile, tier=req.tier)
    report_data = {
        "player_id": req.player_id,
        "player_name": profile["player_name"],
        "generation_method": "fallback_template",
        "sections": report_sections,
        "referenced_metrics": profile["sis_breakdown"],
        "disclaimer": "Based on synthetic data and experimental metrics. All players, clubs, and events are fictional.",
    }
    return api_response(report_data)
