"""
sequences.py — Tactical sequence inspection and counterfactual simulation endpoints.
All data served is synthetic and fictional.
"""
from __future__ import annotations

from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Body
from api.dependencies import get_match_cache, api_response, api_error
from counterfactual.simulator import simulate_counterfactual

router = APIRouter()


class CounterfactualRequest(BaseModel):
    counterfactual_type: str = "remove_movement"


@router.get("/sequences/{sequence_id}")
def get_sequence_detail(sequence_id: str, cache: dict = Depends(get_match_cache)):
    """Retrieve full sequence replay data including 1-second frames, detections, and narrative."""
    seq = cache["sequences"].get(sequence_id)
    if not seq:
        raise api_error("NOT_FOUND", f"Sequence '{sequence_id}' not found")
    return api_response(seq)


@router.post("/sequences/{sequence_id}/counterfactual")
def get_sequence_counterfactual(
    sequence_id: str,
    req: CounterfactualRequest = Body(default_factory=CounterfactualRequest),
    cache: dict = Depends(get_match_cache),
):
    """
    Simulate counterfactual scenario for a sequence (e.g. what if player did not move).
    Returns observed vs counterfactual state comparison and delta metrics.
    """
    cf_key = (sequence_id, req.counterfactual_type)
    if cf_key in cache["counterfactuals"]:
        return api_response(cache["counterfactuals"][cf_key])

    # If not cached, dynamically simulate from sequence data
    seq = cache["sequences"].get(sequence_id)
    if not seq:
        raise api_error("NOT_FOUND", f"Sequence '{sequence_id}' not found")

    cf_result = simulate_counterfactual(seq, seq["focus_player_id"], req.counterfactual_type)
    return api_response(cf_result)
