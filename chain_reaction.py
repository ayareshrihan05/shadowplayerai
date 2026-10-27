"""
chain_reaction.py — Chain reaction impact scoring for ShadowPlayer AI.
Measures the downstream attacking or defensive actions associated with an off-ball movement.
Calculates outcomes occurring within a 10-second window following the movement.
All scoring is deterministic.
"""
from __future__ import annotations

EVENT_WEIGHTS = {
    "pass_forward_complete": 25.0,
    "pass_complete": 15.0,
    "shot_on_target": 40.0,
    "shot": 25.0,
    "goal": 50.0,
    "interception": 30.0,
    "tackle_won": 20.0,
    "possession_won": 25.0,
    "turnover_forced": 20.0,
    "dispossessed": -15.0,
}


def compute_chain_reaction_score(
    movement_end_time: float,
    team_id: str,
    events: list[dict],
    window_seconds: float = 10.0,
) -> float:
    """
    Compute downstream action score within window_seconds of movement end.

    Args:
        movement_end_time: timestamp (s) when movement ended.
        team_id: team of the player who made the movement.
        events: list of match events.
        window_seconds: evaluation window (default 10s).

    Returns:
        Normalized score in [0.0, 100.0].
    """
    window_events = [
        e for e in events
        if movement_end_time <= e["timestamp"] <= movement_end_time + window_seconds
    ]

    if not window_events:
        return 20.0  # Base neutral credit for maintaining play

    raw_score = 20.0  # Base credit

    for e in window_events:
        etype = e.get("event_type", "")
        e_team = e.get("team_id", "")
        meta = e.get("metadata", {})
        is_teammate = (e_team == team_id)

        if etype == "pass" and is_teammate:
            if meta.get("outcome") == "complete":
                if meta.get("is_forward", False):
                    raw_score += EVENT_WEIGHTS["pass_forward_complete"]
                else:
                    raw_score += EVENT_WEIGHTS["pass_complete"]
            elif meta.get("outcome") == "intercepted":
                raw_score += EVENT_WEIGHTS["dispossessed"]

        elif etype == "shot" and is_teammate:
            if meta.get("on_target", False):
                raw_score += EVENT_WEIGHTS["shot_on_target"]
            else:
                raw_score += EVENT_WEIGHTS["shot"]

        elif etype == "interception" and is_teammate:
            raw_score += EVENT_WEIGHTS["interception"]

        elif etype == "tackle" and is_teammate and meta.get("outcome") == "won":
            raw_score += EVENT_WEIGHTS["tackle_won"]

    return max(0.0, min(100.0, round(raw_score, 1)))
