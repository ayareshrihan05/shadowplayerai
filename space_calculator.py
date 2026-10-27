"""
space_calculator.py — Space control and Voronoi area estimation.
Uses scipy cKDTree nearest-neighbour approach on a 2m grid.
All calculations are deterministic and synthetic.
"""
from __future__ import annotations

import numpy as np

try:
    from scipy.spatial import cKDTree
    _HAS_SCIPY = True
except ImportError:
    _HAS_SCIPY = False

PITCH_W = 105.0
PITCH_H = 68.0


def _build_grid(resolution: float = 2.0) -> np.ndarray:
    """Return (N, 2) array of grid cell centres."""
    xs = np.arange(resolution / 2, PITCH_W, resolution)
    ys = np.arange(resolution / 2, PITCH_H, resolution)
    gx, gy = np.meshgrid(xs, ys)
    return np.column_stack([gx.ravel(), gy.ravel()])


def compute_voronoi_areas(
    positions: list[dict],
    grid_resolution: float = 2.0,
) -> dict[str, float]:
    """
    Approximate Voronoi area (m²) controlled by each player using a grid
    nearest-neighbour approach.

    Args:
        positions: list of {player_id, x, y, ...} dicts.
        grid_resolution: grid cell size in meters.

    Returns:
        dict mapping player_id -> area_m2
    """
    if not positions:
        return {}

    grid = _build_grid(grid_resolution)
    cell_area = grid_resolution ** 2

    coords = np.array([[p["x"], p["y"]] for p in positions])
    player_ids = [p["player_id"] for p in positions]

    if _HAS_SCIPY:
        tree = cKDTree(coords)
        _, indices = tree.query(grid)
    else:
        # Fallback: brute-force nearest neighbour
        dists = np.linalg.norm(grid[:, None, :] - coords[None, :, :], axis=2)
        indices = np.argmin(dists, axis=1)

    areas: dict[str, float] = {pid: 0.0 for pid in player_ids}
    for owner_idx in indices:
        areas[player_ids[owner_idx]] += cell_area

    return areas


def compute_zone_control(
    positions: list[dict],
    team_id: str,
    grid_resolution: float = 2.0,
) -> float:
    """
    Estimate the percentage of pitch area controlled by team_id's players.

    Args:
        positions: list of {player_id, team_id, x, y, ...} for ALL players.
        team_id: team to measure.
        grid_resolution: grid cell size in meters.

    Returns:
        float in [0.0, 1.0] representing proportion of pitch.
    """
    if not positions:
        return 0.0

    grid = _build_grid(grid_resolution)
    coords = np.array([[p["x"], p["y"]] for p in positions])
    teams = [p.get("team_id", "") for p in positions]

    if _HAS_SCIPY:
        tree = cKDTree(coords)
        _, indices = tree.query(grid)
    else:
        dists = np.linalg.norm(grid[:, None, :] - coords[None, :, :], axis=2)
        indices = np.argmin(dists, axis=1)

    team_cells = sum(1 for idx in indices if teams[idx] == team_id)
    return round(team_cells / len(grid), 4)


def compute_space_created(
    positions_before: list[dict],
    positions_after: list[dict],
    player_id: str,
    grid_resolution: float = 2.0,
) -> float:
    """
    Estimate space created by player_id between two frames.
    Returns the change in the player's Voronoi area (m²). Positive = more space.
    """
    before = compute_voronoi_areas(positions_before, grid_resolution)
    after = compute_voronoi_areas(positions_after, grid_resolution)
    area_before = before.get(player_id, 0.0)
    area_after = after.get(player_id, 0.0)
    return round(area_after - area_before, 2)
