"""
narrative_service.py — AI narrative generation orchestrator.
Attempts Microsoft Foundry generation, validates against verified analytics metrics,
and automatically falls back to deterministic templates if AI is disabled or invalid.
"""
from __future__ import annotations

import logging
from typing import Any

from ai.ms_foundry_client import call_foundry
from ai.fallback_templates import generate_fallback_report
from ai.output_validator import validate_ai_report

logger = logging.getLogger("shadowplayer.ai")

DISCLAIMER_TEXT = "Based on synthetic data and experimental metrics. All players, clubs, and events are fictional."


async def generate_scouting_report(
    profile: dict,
    tier: str = "analyst",
) -> dict:
    """
    Generate an AI scouting report for a player.
    Returns dict matching ScoutingReport Pydantic schema:
      player_id: str
      player_name: str
      generation_method: str ("ms_foundry" or "fallback_template")
      sections: ReportSections dict
      referenced_metrics: dict[str, float]
      disclaimer: str
    """
    pid = profile.get("player_id", "")
    pname = profile.get("player_name", "Unknown Player")
    sis_data = profile.get("sis_breakdown", {})
    verified_metrics = {
        "sis": sis_data.get("sis", 50.0),
        "space_creation_score": sis_data.get("space_creation_score", 50.0),
        "passing_lane_score": sis_data.get("passing_lane_score", 50.0),
        "defensive_support_score": sis_data.get("defensive_support_score", 50.0),
        "chain_reaction_score": sis_data.get("chain_reaction_score", 50.0),
    }

    # Attempt Microsoft Foundry if available
    generation_method = "fallback_template"
    sections = None

    prompt = (
        f"Generate a football scouting report for fictional player {pname} ({profile.get('position')}). "
        f"Verified metrics from synthetic tracking data: "
        f"Overall SIS: {verified_metrics['sis']}/100, "
        f"Space Creation: {verified_metrics['space_creation_score']}, "
        f"Passing Lane Creation: {verified_metrics['passing_lane_score']}, "
        f"Defensive Support: {verified_metrics['defensive_support_score']}, "
        f"Chain Reaction: {verified_metrics['chain_reaction_score']}. "
        f"Audience tier: {tier}."
    )

    ai_response = await call_foundry(prompt)
    if ai_response:
        is_valid, reason = validate_ai_report(ai_response, [pname], verified_metrics)
        if is_valid:
            generation_method = "ms_foundry"
            sections = {
                "overview": ai_response[:300],
                "off_ball_strengths": f"Strong spatial exploitation (S={verified_metrics['space_creation_score']}).",
                "key_sequences": "Decoy and passing lane movements recorded across synthetic match phases.",
                "defensive_contributions": f"Defensive support rated at {verified_metrics['defensive_support_score']}/100.",
                "attacking_contributions": f"Chain reaction downstream impact: {verified_metrics['chain_reaction_score']}/100.",
                "improvement_areas": "Sustained high-tempo positional adjustments during fast transitions.",
                "limitations": "Generated from synthetic Premier League-style tracking data.",
            }
        else:
            logger.info("Foundry output failed validation (%s) — using fallback template.", reason)

    if not sections:
        sections = generate_fallback_report(profile, tier=tier)

    return {
        "player_id": pid,
        "player_name": pname,
        "generation_method": generation_method,
        "sections": sections,
        "referenced_metrics": verified_metrics,
        "disclaimer": DISCLAIMER_TEXT,
    }


def generate_scouting_report_sync(
    profile: dict,
    tier: str = "analyst",
) -> dict:
    """Synchronous fallback scouting report generator."""
    pid = profile.get("player_id", "")
    pname = profile.get("player_name", "Unknown Player")
    sis_data = profile.get("sis_breakdown", {})
    verified_metrics = {
        "sis": sis_data.get("sis", 50.0),
        "space_creation_score": sis_data.get("space_creation_score", 50.0),
        "passing_lane_score": sis_data.get("passing_lane_score", 50.0),
        "defensive_support_score": sis_data.get("defensive_support_score", 50.0),
        "chain_reaction_score": sis_data.get("chain_reaction_score", 50.0),
    }
    sections = generate_fallback_report(profile, tier=tier)
    return {
        "player_id": pid,
        "player_name": pname,
        "generation_method": "fallback_template",
        "sections": sections,
        "referenced_metrics": verified_metrics,
        "disclaimer": DISCLAIMER_TEXT,
    }
