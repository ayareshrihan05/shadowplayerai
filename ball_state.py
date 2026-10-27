"""
ball_state.py — Ball position management for procedural match sections.
All data is synthetic and fictional.

Coordinate system: (0,0) bottom-left, (105,68) top-right, meters.
"""
from __future__ import annotations

import math
import numpy as np

PITCH_W = 105.0
PITCH_H = 68.0

# Scenario timestamp ranges — do not override ball in these windows
SCENARIO_RANGES = [
    (360, 375),
    (2302, 2320),
    (4330, 4348),
]


def _is_in_scenario(t: float) -> bool:
    for start, end in SCENARIO_RANGES:
        if start <= t <= end:
            return True
    return False


def _clamp(val: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, val))


def _lerp(a: float, b: float, frac: float) -> float:
    return a + (b - a) * frac


def _ball_between_players(
    from_x: float, from_y: float,
    to_x: float, to_y: float,
    frac: float,
) -> tuple[float, float]:
    """Interpolated ball position during a pass."""
    return (_lerp(from_x, to_x, frac), _lerp(from_y, to_y, frac))


def generate_ball_states(
    duration_seconds: int,
    rng: np.random.Generator,
    all_player_positions: dict[float, list[dict]],
    events: list[dict],
) -> dict[float, dict]:
    """
    Generate ball state for each second of the match (excluding scenario windows).

    Returns: dict mapping timestamp -> BallState dict
      {x, y, vx, vy, z, speed}
    """
    # Build pass event lookup by timestamp
    pass_events = [e for e in events if e["event_type"] == "pass" and not _is_in_scenario(e["timestamp"])]
    pass_by_t: dict[float, dict] = {e["timestamp"]: e for e in pass_events}

    ball_states: dict[float, dict] = {}

    # Starting ball position (centre circle)
    bx, by = 52.5, 34.0
    bvx, bvy = 0.0, 0.0

    t = 0.0
    while t <= duration_seconds:
        if _is_in_scenario(t):
            t += 1.0
            continue

        # Check if a pass starts at this timestamp
        if t in pass_by_t:
            evt = pass_by_t[t]
            src = evt["location"]
            tgt = evt["metadata"].get("target_location", {"x": src["x"] + 10, "y": src["y"]})
            dx = tgt["x"] - src["x"]
            dy = tgt["y"] - src["y"]
            dist = math.sqrt(dx * dx + dy * dy) or 1.0
            pass_speed = min(15.0, dist / 1.5)  # arrive in ~1.5s
            bvx = dx / 1.5
            bvy = dy / 1.5
            bx = src["x"]
            by = src["y"]
        else:
            # Ball drifts with possession holder or slows to stop
            speed = math.sqrt(bvx**2 + bvy**2)
            if speed > 0.1:
                decel = min(speed, 3.0)
                bvx *= (1.0 - decel / speed) if speed > 0 else 0.0
                bvy *= (1.0 - decel / speed) if speed > 0 else 0.0
                bx = _clamp(bx + bvx, 0.5, PITCH_W - 0.5)
                by = _clamp(by + bvy, 0.5, PITCH_H - 0.5)
            else:
                bvx, bvy = 0.0, 0.0
                # Occasionally pick a new carrier from player positions at this t
                if rng.random() < 0.02:
                    plist = all_player_positions.get(t, [])
                    if plist:
                        carrier = rng.choice(plist)
                        bx = carrier["x"] + rng.uniform(-0.5, 0.5)
                        by = carrier["y"] + rng.uniform(-0.5, 0.5)

        ball_states[t] = {
            "x": round(bx, 2),
            "y": round(by, 2),
            "vx": round(bvx, 3),
            "vy": round(bvy, 3),
            "z": 0.0,
            "speed": round(math.sqrt(bvx**2 + bvy**2), 3),
        }

        t += 1.0

    return ball_states
