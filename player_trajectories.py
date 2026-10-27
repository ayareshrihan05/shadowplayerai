"""
player_trajectories.py — Role-appropriate procedural movement generator.
Generates realistic player positions for non-scenario match periods.
All coordinates are synthetic and fictional.

Coordinate system: (0,0) bottom-left, (105,68) top-right, meters.
Northvale FC attacks left-to-right (increasing x).
"""
from __future__ import annotations

import math
from typing import NamedTuple

import numpy as np

# Pitch boundaries
PITCH_W = 105.0
PITCH_H = 68.0

# Speed bands (m/s)
SPEED_WALK = (0.0, 1.5)
SPEED_JOG = (1.5, 3.5)
SPEED_RUN = (3.5, 6.5)
SPEED_SPRINT = (6.5, 9.0)

# Scenario timestamp ranges to avoid overwriting
SCENARIO_RANGES = [
    (360, 375),
    (2302, 2320),
    (4330, 4348),
]

# Position zone bounds (x_min, x_max, y_min, y_max) — approximate areas per role
POSITION_ZONES: dict[str, tuple[float, float, float, float]] = {
    "GK":  (2.0,  18.0, 20.0, 48.0),
    "CB":  (15.0, 45.0, 18.0, 52.0),
    "LB":  (20.0, 60.0, 44.0, 66.0),
    "RB":  (20.0, 60.0,  2.0, 24.0),
    "DM":  (35.0, 60.0, 22.0, 46.0),
    "CM":  (38.0, 68.0, 18.0, 52.0),
    "CAM": (52.0, 78.0, 20.0, 50.0),
    "LW":  (55.0, 95.0, 46.0, 66.0),
    "RW":  (55.0, 95.0,  2.0, 22.0),
    "ST":  (60.0, 98.0, 22.0, 46.0),
}

# Away team uses mirrored x-zones (attacks right-to-left)
AWAY_POSITION_ZONES: dict[str, tuple[float, float, float, float]] = {
    pos: (PITCH_W - z[1], PITCH_W - z[0], z[2], z[3])
    for pos, z in POSITION_ZONES.items()
}


class TrajectoryFrame(NamedTuple):
    t: float
    x: float
    y: float
    vx: float
    vy: float
    speed: float


def _clamp(val: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, val))


def _is_in_scenario(t: float) -> bool:
    """Return True if timestamp t falls inside any pre-built scenario range."""
    for start, end in SCENARIO_RANGES:
        if start <= t <= end:
            return True
    return False


def _get_zone(position: str, team_id: str) -> tuple[float, float, float, float]:
    """Return (x_min, x_max, y_min, y_max) for the given position and team."""
    zones = AWAY_POSITION_ZONES if "eastmere" in team_id else POSITION_ZONES
    return zones.get(position, (20.0, 85.0, 10.0, 58.0))


def _smooth_random_walk(
    rng: np.random.Generator,
    start_x: float,
    start_y: float,
    zone: tuple[float, float, float, float],
    n_frames: int,
    speed_band: tuple[float, float] = SPEED_JOG,
    direction_change_prob: float = 0.12,
) -> list[TrajectoryFrame]:
    """
    Generate a smooth random-walk trajectory staying within zone bounds.
    Returns a list of TrajectoryFrame with sequential integer timestamps starting at 0.
    Timestamps must be offset by caller.
    """
    x_min, x_max, y_min, y_max = zone
    x, y = _clamp(start_x, x_min, x_max), _clamp(start_y, y_min, y_max)

    speed = rng.uniform(*speed_band)
    angle = rng.uniform(0, 2 * math.pi)

    frames: list[TrajectoryFrame] = []

    for i in range(n_frames):
        # Possibly change direction
        if rng.random() < direction_change_prob:
            angle += rng.uniform(-math.pi / 3, math.pi / 3)
            speed = rng.uniform(*speed_band)

        # Steer away from boundaries
        if x < x_min + 3.0:
            angle = rng.uniform(-math.pi / 4, math.pi / 4)
        elif x > x_max - 3.0:
            angle = rng.uniform(3 * math.pi / 4, 5 * math.pi / 4)
        if y < y_min + 3.0:
            angle = rng.uniform(0, math.pi)
        elif y > y_max - 3.0:
            angle = rng.uniform(math.pi, 2 * math.pi)

        vx = speed * math.cos(angle)
        vy = speed * math.sin(angle)

        frames.append(TrajectoryFrame(t=float(i), x=round(x, 2), y=round(y, 2),
                                      vx=round(vx, 3), vy=round(vy, 3),
                                      speed=round(speed, 3)))

        x = _clamp(x + vx, x_min, x_max)
        y = _clamp(y + vy, y_min, y_max)

    return frames


def generate_trajectory(
    player_id: str,
    position: str,
    team_id: str,
    start_x: float,
    start_y: float,
    duration_seconds: int,
    rng: np.random.Generator,
    t_offset: float = 0.0,
) -> list[dict]:
    """
    Generate a full-match trajectory for a single player for non-scenario periods.

    Returns a list of dicts: {t, x, y, vx, vy, speed}
    Only returns frames where _is_in_scenario(t) is False.
    """
    zone = _get_zone(position, team_id)

    # GKs move very little
    if position == "GK":
        speed_band = SPEED_WALK
        dir_change_prob = 0.05
    elif position in ("CB", "DM"):
        speed_band = SPEED_JOG
        dir_change_prob = 0.08
    elif position in ("CM", "CAM"):
        speed_band = SPEED_JOG
        dir_change_prob = 0.12
    elif position in ("LB", "RB"):
        speed_band = (1.0, 4.5)
        dir_change_prob = 0.14
    else:  # LW, RW, ST
        speed_band = (1.5, 5.0)
        dir_change_prob = 0.15

    raw_frames = _smooth_random_walk(
        rng=rng,
        start_x=start_x,
        start_y=start_y,
        zone=zone,
        n_frames=duration_seconds,
        speed_band=speed_band,
        direction_change_prob=dir_change_prob,
    )

    result = []
    for frame in raw_frames:
        t = t_offset + frame.t
        if not _is_in_scenario(t):
            result.append({
                "t": t,
                "x": frame.x,
                "y": frame.y,
                "vx": frame.vx,
                "vy": frame.vy,
                "speed": frame.speed,
                "player_id": player_id,
            })

    return result


def build_frame_player_positions(
    all_player_trajectories: dict[str, list[dict]],
    t: float,
) -> list[dict]:
    """
    Given all player trajectories (keyed by player_id), return the PlayerPosition list
    for a single timestamp t. Uses nearest frame if exact t not present.
    """
    positions = []
    for player_id, frames in all_player_trajectories.items():
        if not frames:
            continue
        # Find closest frame by time
        closest = min(frames, key=lambda f: abs(f["t"] - t))
        positions.append({
            "player_id": player_id,
            "x": closest["x"],
            "y": closest["y"],
            "vx": closest["vx"],
            "vy": closest["vy"],
            "speed": closest["speed"],
            "is_in_possession": False,
        })
    return positions
