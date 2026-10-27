"""
match_generator.py — Main match orchestrator for ShadowPlayer AI.
Generates a complete synthetic football match with:
  - Fixed 22-player roster (strictly segregated by gender)
  - Pre-designed tactical scenarios at fixed timestamps
  - Procedurally generated background frames and events

All data is synthetic and fictional.
"""
from __future__ import annotations

import datetime
from typing import Any

import numpy as np

from simulator.scenarios import (
    MEN_HOME_TEAM, MEN_AWAY_TEAM, MEN_ALL_PLAYERS, MEN_SCENARIOS, MEN_SCENARIO_EVENTS,
    WOMEN_HOME_TEAM, WOMEN_AWAY_TEAM, WOMEN_ALL_PLAYERS, WOMEN_SCENARIOS, WOMEN_SCENARIO_EVENTS,
    HOME_TEAM, AWAY_TEAM, ALL_PLAYERS,
    HOME_FORMATION_POSITIONS, AWAY_FORMATION_POSITIONS,
    ALL_SCENARIOS, ALL_SCENARIO_EVENTS,
)
from simulator.player_trajectories import generate_trajectory
from simulator.event_generator import generate_procedural_events

MATCH_ID = "match-men-001"
PITCH_W = 105.0
PITCH_H = 68.0


def _build_sis_leaderboard(all_players: list[dict]) -> list[dict]:
    """Placeholder leaderboard with initial values — replaced after analytics run."""
    leaderboard = []
    pre = {
        "p001": 56.7, "p010": 50.8, "p004": 55.1,
        "w002": 58.2, "w010": 54.0, "w001": 51.5,
    }
    for p in all_players:
        leaderboard.append({
            "player_id": p["player_id"],
            "name": p["name"],
            "sis": pre.get(p["player_id"], round(30.0 + (hash(p["player_id"]) % 20), 1)),
            "position": p["position"],
            "confidence": 0.82 if p["player_id"] in pre else 0.55,
        })
    leaderboard.sort(key=lambda x: x["sis"], reverse=True)
    return leaderboard


def generate_match(
    seed: int = 42,
    duration_seconds: int = 5400,
    match_id: str = "match-alpha-001",
    home_team: dict | None = None,
    away_team: dict | None = None,
    scenarios: list[dict] | None = None,
    scenario_events: list[dict] | None = None,
) -> dict:
    """
    Generate a complete synthetic match dict matching MatchSummary + MatchDetail structure.

    Returns:
        dict with keys: match_id, home_team, away_team, duration_seconds, generated_at,
                        seed, event_count, frame_count, scenario_count, sis_leaderboard,
                        frames (list of FrameData dicts), events (list of event dicts),
                        scenarios (list of scenario dicts), data_label
    """
    rng = np.random.default_rng(seed)

    is_women = ("women" in match_id) or (home_team and "women" in home_team.get("team_id", ""))

    if home_team is None:
        home_team = WOMEN_HOME_TEAM if is_women else MEN_HOME_TEAM
    if away_team is None:
        away_team = WOMEN_AWAY_TEAM if is_women else MEN_AWAY_TEAM
    if scenarios is None:
        if match_id == "match-women-001":
            scenarios = WOMEN_SCENARIOS
        elif match_id == "match-men-001":
            scenarios = MEN_SCENARIOS
        else:
            scenarios = ALL_SCENARIOS
    if scenario_events is None:
        if match_id == "match-women-001":
            scenario_events = WOMEN_SCENARIO_EVENTS
        elif match_id == "match-men-001":
            scenario_events = MEN_SCENARIO_EVENTS
        else:
            scenario_events = ALL_SCENARIO_EVENTS

    roster = home_team["players"] + away_team["players"]

    # Scenario timestamp windows
    scenario_ranges = [(int(s["timestamp_start"]), int(s["timestamp_end"])) for s in scenarios]

    def _is_in_scenario(t: float) -> bool:
        for start, end in scenario_ranges:
            if start <= t <= end:
                return True
        return False

    # ── Step 1: Build player trajectories for non-scenario periods ────────────
    all_trajectories: dict[str, list[dict]] = {}

    for player in roster:
        pid = player["player_id"]
        team_id = player["team_id"]
        position = player["position"]

        if "northvale" in team_id:
            sx, sy = HOME_FORMATION_POSITIONS.get(pid, (52.5, 34.0))
        else:
            sx, sy = AWAY_FORMATION_POSITIONS.get(pid, (52.5, 34.0))

        traj = generate_trajectory(
            player_id=pid,
            position=position,
            team_id=team_id,
            start_x=sx,
            start_y=sy,
            duration_seconds=duration_seconds,
            rng=rng,
            t_offset=0.0,
        )
        all_trajectories[pid] = traj

    # Build time-indexed position lookup for procedural periods
    player_pos_by_t: dict[float, list[dict]] = {}
    for t in range(0, duration_seconds + 1, 10):
        if _is_in_scenario(float(t)):
            continue
        frame_players = []
        for pid, traj in all_trajectories.items():
            if not traj:
                continue
            closest = min(traj, key=lambda f: abs(f["t"] - t))
            frame_players.append({
                "player_id": pid,
                "x": closest["x"],
                "y": closest["y"],
                "vx": closest["vx"],
                "vy": closest["vy"],
                "speed": closest["speed"],
                "is_in_possession": False,
            })
        player_pos_by_t[float(t)] = frame_players

    # ── Step 2: Generate procedural events ───────────────────────────────────
    procedural_events = generate_procedural_events(
        rng=rng,
        duration_seconds=duration_seconds,
        match_id=match_id,
        is_women=is_women,
    )

    # Combine with scenario events
    all_events = list(scenario_events) + procedural_events
    all_events.sort(key=lambda e: e["timestamp"])

    # ── Step 3: Merge scenario frames with procedural frames ─────────────────
    all_frames: list[dict] = []

    # Procedural frames (every 30 seconds, skipping scenario windows)
    for t in range(0, duration_seconds + 1, 30):
        if _is_in_scenario(float(t)):
            continue
        closest_t = min(player_pos_by_t.keys(), key=lambda pt: abs(pt - t)) if player_pos_by_t else None
        players_at_t = player_pos_by_t.get(closest_t, []) if closest_t is not None else []

        carrier_id = None
        nearby_events = [e for e in all_events if abs(e["timestamp"] - t) < 30 and e["event_type"] == "pass"]
        if nearby_events:
            carrier_id = nearby_events[0]["player_id"]
            for p in players_at_t:
                p["is_in_possession"] = (p["player_id"] == carrier_id)

        if carrier_id:
            carrier_pos = next((p for p in players_at_t if p["player_id"] == carrier_id), None)
            bx = carrier_pos["x"] if carrier_pos else PITCH_W / 2
            by = carrier_pos["y"] if carrier_pos else PITCH_H / 2
        else:
            bx, by = PITCH_W / 2, PITCH_H / 2

        all_frames.append({
            "t": float(t),
            "players": players_at_t,
            "ball": {"x": round(bx, 2), "y": round(by, 2), "vx": 0.0, "vy": 0.0, "z": 0.0, "speed": 0.0},
            "passing_lanes": [],
            "open_space_zones": [],
        })

    # Inject scenario frames
    for scenario in scenarios:
        all_frames.extend(scenario["frames"])

    # Sort all frames by timestamp
    all_frames.sort(key=lambda f: f["t"])

    # ── Step 4: Assemble match record ────────────────────────────────────────
    generated_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

    match_record = {
        "match_id": match_id,
        "home_team": home_team,
        "away_team": away_team,
        "duration_seconds": duration_seconds,
        "generated_at": generated_at,
        "seed": seed,
        "event_count": len(all_events),
        "frame_count": len(all_frames),
        "scenario_count": len(scenarios),
        "sis_leaderboard": _build_sis_leaderboard(roster),
        "frames": all_frames,
        "events": all_events,
        "scenarios": scenarios,
        "data_label": "SYNTHETIC MATCH — FICTIONAL",
    }

    return match_record
