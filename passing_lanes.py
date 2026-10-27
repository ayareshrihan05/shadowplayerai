"""
passing_lanes.py — Passing lane geometry for ShadowPlayer AI analytics.
Uses point-to-line-segment distance checks to detect corridor intersections.
All calculations are deterministic and work on synthetic tracking data.
"""
from __future__ import annotations

import math

PITCH_W = 105.0
PITCH_H = 68.0


def _dist_point_to_segment(
    px: float, py: float,
    ax: float, ay: float,
    bx: float, by: float,
) -> float:
    """
    Minimum distance from point (px, py) to line segment (ax, ay)-(bx, by).
    """
    abx, aby = bx - ax, by - ay
    ab_len_sq = abx * abx + aby * aby
    if ab_len_sq < 1e-9:
        return math.sqrt((px - ax) ** 2 + (py - ay) ** 2)
    t = max(0.0, min(1.0, ((px - ax) * abx + (py - ay) * aby) / ab_len_sq))
    cx, cy = ax + t * abx, ay + t * aby
    return math.sqrt((px - cx) ** 2 + (py - cy) ** 2)


def is_lane_blocked(
    carrier_x: float, carrier_y: float,
    target_x: float, target_y: float,
    opponent_positions: list[dict],
    lane_width: float = 1.5,
) -> tuple[bool, float]:
    """
    Check if any opponent blocks the lane between carrier and target.

    Args:
        carrier_x/y: ball carrier position.
        target_x/y: intended pass recipient position.
        opponent_positions: list of {player_id, x, y} for opponents.
        lane_width: half-width of the corridor in meters.

    Returns:
        (blocked: bool, min_clearance: float) — min_clearance is the minimum
        distance any opponent is from the lane centreline.
    """
    min_clearance = float("inf")
    for opp in opponent_positions:
        d = _dist_point_to_segment(
            opp["x"], opp["y"],
            carrier_x, carrier_y,
            target_x, target_y,
        )
        min_clearance = min(min_clearance, d)

    if not opponent_positions:
        min_clearance = lane_width + 10.0

    blocked = min_clearance < lane_width
    return blocked, round(min_clearance, 2)


def compute_passing_lanes(
    carrier_pos: dict,
    teammates: list[dict],
    opponents: list[dict],
    lane_width: float = 1.5,
    max_range: float = 30.0,
) -> list[dict]:
    """
    Compute all potential passing lanes from carrier to each teammate.

    Args:
        carrier_pos: {player_id, x, y} of ball carrier.
        teammates: list of {player_id, x, y} for eligible recipients.
        opponents: list of {player_id, x, y} for defenders.
        lane_width: half-width of passing corridor in meters.
        max_range: maximum pass distance to consider.

    Returns:
        list of PassingLane dicts: {from_player, to_player, blocked, width, length}
    """
    lanes = []
    cx, cy = carrier_pos["x"], carrier_pos["y"]

    for tm in teammates:
        tx, ty = tm["x"], tm["y"]
        length = math.sqrt((tx - cx) ** 2 + (ty - cy) ** 2)

        if length < 1.0 or length > max_range:
            continue

        bx_min = min(cx, tx) - lane_width * 2
        bx_max = max(cx, tx) + lane_width * 2
        by_min = min(cy, ty) - lane_width * 2
        by_max = max(cy, ty) + lane_width * 2
        relevant_opps = [
            o for o in opponents
            if bx_min <= o["x"] <= bx_max and by_min <= o["y"] <= by_max
        ]

        blocked, min_clearance = is_lane_blocked(cx, cy, tx, ty, relevant_opps, lane_width)
        effective_width = min(min_clearance * 2, lane_width * 4) if not blocked else min_clearance * 2

        lanes.append({
            "from_player": carrier_pos["player_id"],
            "to_player": tm["player_id"],
            "blocked": blocked,
            "width": round(effective_width, 2),
            "length": round(length, 2),
        })

    lanes.sort(key=lambda l: (l["blocked"], l["length"]))
    return lanes


def count_open_lanes(lanes: list[dict]) -> int:
    """Return count of unblocked passing lanes."""
    return sum(1 for l in lanes if not l["blocked"])


def average_lane_width(lanes: list[dict]) -> float:
    """Return average width of unblocked lanes, or 0.0 if none."""
    open_lanes = [l for l in lanes if not l["blocked"]]
    if not open_lanes:
        return 0.0
    return round(sum(l["width"] for l in open_lanes) / len(open_lanes), 2)
