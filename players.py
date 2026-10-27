"""
players.py — Player Shadow Profile and player movement sequence endpoints.
All data served is synthetic and fictional.
"""
from __future__ import annotations

from typing import Optional
from fastapi import APIRouter, Depends, Query
from api.dependencies import get_match_cache, api_response, api_error

router = APIRouter()


@router.get("/players/{player_id}/shadow-profile")
def get_shadow_profile(
    player_id: str,
    match_id: str = "match-alpha-001",
    cache: dict = Depends(get_match_cache),
):
    """Retrieve full Shadow Profile for a player in a specific match."""
    profile = cache["profiles"].get((player_id, match_id))
    if not profile:
        raise api_error("NOT_FOUND", f"Profile for player '{player_id}' in match '{match_id}' not found")
    return api_response(profile)


@router.get("/players/{player_id}/sequences")
def get_player_sequences(
    player_id: str,
    match_id: str = "match-alpha-001",
    movement_type: Optional[str] = None,
    cache: dict = Depends(get_match_cache),
):
    """Retrieve tactical sequences involving the specified player."""
    profile = cache["profiles"].get((player_id, match_id))
    if not profile:
        raise api_error("NOT_FOUND", f"Player '{player_id}' not found in match '{match_id}'")

    matched_sequences = []
    # Check prebuilt sequences where player is focus
    for seq_id, seq in cache["sequences"].items():
        if seq["focus_player_id"] == player_id:
            if movement_type and not isinstance(movement_type, type(Depends())):
                dets = [d for d in seq.get("movement_detections", []) if d.get("movement_type") == movement_type]
                if not dets:
                    continue
            matched_sequences.append(seq)

    # If no prebuilt scenario matched, return player's logged sequence summaries as lightweight sequence structures
    if not matched_sequences:
        for seq_summary in profile.get("top_sequences", []):
            if movement_type and seq_summary.get("movement_type") != movement_type:
                continue
            matched_sequences.append({
                "sequence_id": seq_summary["sequence_id"],
                "name": seq_summary["name"],
                "match_id": match_id,
                "focus_player_id": player_id,
                "timestamp_start": seq_summary["timestamp_start"],
                "timestamp_end": seq_summary["timestamp_end"],
                "frames": [],
                "key_events": [],
                "movement_detections": [],
                "ai_explanation": {
                    "text": f"Movement detected: {seq_summary['name']} at t={seq_summary['timestamp_start']:.0f}s.",
                    "evidence_refs": [],
                    "generation_method": "fallback_template",
                    "disclaimer": "Synthetic data.",
                },
            })

    return api_response(matched_sequences)
