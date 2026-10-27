"""
event_generator.py — Procedural football event generator.
Generates synthetic events outside pre-designed scenario windows.
All events are fictional and for demonstration only.

Targets: ≥150 total events, ≥5 instances of each of 7 movement categories.
"""
from __future__ import annotations

import math
import uuid
from typing import Any

import numpy as np

MATCH_ID = "match-alpha-001"
PITCH_W = 105.0
PITCH_H = 68.0

# Scenario timestamp ranges — do not generate events in these windows
SCENARIO_RANGES = [(360, 375), (2302, 2320), (4330, 4348)]
# Last scenario event IDs used (approximate next available base)
SCENARIO_EVENT_COUNT = 11  # evt-0142 to evt-0420 (scenario)


def _is_in_scenario(t: float) -> bool:
    for start, end in SCENARIO_RANGES:
        if start - 5 <= t <= end + 5:
            return True
    return False


def _clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def _dist(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def _rand_pos(rng: np.random.Generator, x_range: tuple, y_range: tuple) -> tuple[float, float]:
    return (round(rng.uniform(*x_range), 1), round(rng.uniform(*y_range), 1))


HOME_PLAYERS = ["p001", "p002", "p003", "p004", "p005", "p006", "p007", "p008", "p009", "p010", "p011"]
AWAY_PLAYERS = ["p012", "p013", "p014", "p015", "p016", "p017", "p018", "p019", "p020", "p021", "p022"]
WOMEN_HOME_PLAYERS = [f"w{i:03d}" for i in range(1, 12)]
WOMEN_AWAY_PLAYERS = [f"w{i:03d}" for i in range(12, 23)]

ALL_PLAYERS = HOME_PLAYERS + AWAY_PLAYERS
PLAYER_TEAM = {p: "team-northvale-fc" for p in HOME_PLAYERS}
PLAYER_TEAM.update({p: "team-eastmere-city" for p in AWAY_PLAYERS})
PLAYER_TEAM.update({w: "team-northvale-women" for w in WOMEN_HOME_PLAYERS})
PLAYER_TEAM.update({w: "team-eastmere-women" for w in WOMEN_AWAY_PLAYERS})

PLAYER_POS = {
    "p001": "ST", "p002": "LW", "p003": "CAM", "p004": "CM", "p005": "CM",
    "p006": "DM", "p007": "RB", "p008": "CB", "p009": "CB", "p010": "LB", "p011": "GK",
    "p012": "ST", "p013": "RW", "p014": "CAM", "p015": "CM", "p016": "CM",
    "p017": "DM", "p018": "RB", "p019": "CB", "p020": "CB", "p021": "LB", "p022": "GK",
}
for k, v in list(PLAYER_POS.items()):
    PLAYER_POS[k.replace("p", "w")] = v


def _evt_id(idx: int, prefix: str = "evt") -> str:
    return f"{prefix}-{idx:04d}"


def _make_pass(
    idx: int, t: float, player_id: str,
    from_x: float, from_y: float,
    to_x: float, to_y: float,
    match_id: str = MATCH_ID,
    outcome: str = "complete",
    pressure: bool = False,
    forward: bool = True,
    tags: list[str] | None = None,
) -> dict:
    prefix = "wevt" if "women" in match_id else "evt"
    return {
        "event_id": _evt_id(idx, prefix),
        "match_id": match_id,
        "timestamp": round(t, 1),
        "frame_id": f"frm-{int(t):04d}",
        "event_type": "pass",
        "player_id": player_id,
        "team_id": PLAYER_TEAM.get(player_id, "team-northvale-fc"),
        "location": {"x": from_x, "y": from_y},
        "metadata": {
            "target_location": {"x": to_x, "y": to_y},
            "outcome": outcome,
            "pass_length": round(_dist(from_x, from_y, to_x, to_y), 1),
            "is_forward": forward,
            "pressure_applied": pressure,
        },
        "sequence_tags": tags or [],
    }


def _make_run(idx: int, t: float, player_id: str, x: float, y: float, run_type: str, match_id: str = MATCH_ID, tags: list[str] | None = None) -> dict:
    prefix = "wevt" if "women" in match_id else "evt"
    return {
        "event_id": _evt_id(idx, prefix),
        "match_id": match_id,
        "timestamp": round(t, 1),
        "frame_id": f"frm-{int(t):04d}",
        "event_type": "run_start",
        "player_id": player_id,
        "team_id": PLAYER_TEAM.get(player_id, "team-northvale-fc"),
        "location": {"x": x, "y": y},
        "metadata": {"run_type": run_type, "trigger_event_id": None},
        "sequence_tags": tags or [],
    }


def _make_tackle(idx: int, t: float, player_id: str, x: float, y: float, match_id: str = MATCH_ID) -> dict:
    prefix = "wevt" if "women" in match_id else "evt"
    return {
        "event_id": _evt_id(idx, prefix),
        "match_id": match_id,
        "timestamp": round(t, 1),
        "frame_id": f"frm-{int(t):04d}",
        "event_type": "tackle",
        "player_id": player_id,
        "team_id": PLAYER_TEAM.get(player_id, "team-northvale-fc"),
        "location": {"x": x, "y": y},
        "metadata": {"outcome": "won"},
        "sequence_tags": [],
    }


def _make_shot(idx: int, t: float, player_id: str, x: float, y: float, on_target: bool, match_id: str = MATCH_ID) -> dict:
    prefix = "wevt" if "women" in match_id else "evt"
    return {
        "event_id": _evt_id(idx, prefix),
        "match_id": match_id,
        "timestamp": round(t, 1),
        "frame_id": f"frm-{int(t):04d}",
        "event_type": "shot",
        "player_id": player_id,
        "team_id": PLAYER_TEAM.get(player_id, "team-northvale-fc"),
        "location": {"x": x, "y": y},
        "metadata": {"on_target": on_target, "outcome": "saved" if on_target else "off_target"},
        "sequence_tags": [],
    }


def _make_press(idx: int, t: float, player_id: str, x: float, y: float, target_id: str, match_id: str = MATCH_ID) -> dict:
    prefix = "wevt" if "women" in match_id else "evt"
    return {
        "event_id": _evt_id(idx, prefix),
        "match_id": match_id,
        "timestamp": round(t, 1),
        "frame_id": f"frm-{int(t):04d}",
        "event_type": "press_start",
        "player_id": player_id,
        "team_id": PLAYER_TEAM.get(player_id, "team-northvale-fc"),
        "location": {"x": x, "y": y},
        "metadata": {"target_player_id": target_id},
        "sequence_tags": [],
    }


def _make_change_dir(idx: int, t: float, player_id: str, x: float, y: float, response_to: str, match_id: str = MATCH_ID) -> dict:
    prefix = "wevt" if "women" in match_id else "evt"
    return {
        "event_id": _evt_id(idx, prefix),
        "match_id": match_id,
        "timestamp": round(t, 1),
        "frame_id": f"frm-{int(t):04d}",
        "event_type": "change_direction",
        "player_id": player_id,
        "team_id": PLAYER_TEAM.get(player_id, "team-northvale-fc"),
        "location": {"x": x, "y": y},
        "metadata": {"response_to": response_to, "direction": "lateral"},
        "sequence_tags": [],
    }


def generate_procedural_events(
    rng: np.random.Generator,
    duration_seconds: int = 5400,
    match_id: str = MATCH_ID,
    is_women: bool = False,
) -> list[dict]:
    """
    Generate ≥150 procedural events at timestamps outside scenario windows.
    Ensures ≥5 detectable instances of each of 7 movement categories:
      decoy_run, diagonal_run, overlapping_run, free_space_movement,
      defensive_tracking, covering_run, pressing_movement
    """
    if "women" in match_id:
        is_women = True

    h_players = WOMEN_HOME_PLAYERS if is_women else HOME_PLAYERS
    a_players = WOMEN_AWAY_PLAYERS if is_women else AWAY_PLAYERS

    def _p(pid: str) -> str:
        return pid.replace("p", "w") if is_women else pid

    events: list[dict] = []
    idx = 500  # Start well above scenario event IDs (max ~evt-0420)

    # ── Phase 1: Guaranteed movement category coverage (≥5 each) ──────────────

    # 1. Decoy runs (5 instances) — ST or LW without ball reception
    decoy_timestamps = [180, 720, 1440, 3000, 4200]
    decoy_players = [_p(p) for p in ["p001", "p002", "p001", "p002", "p001"]]
    for ts, pid in zip(decoy_timestamps, decoy_players):
        if _is_in_scenario(ts):
            ts += 30
        x, y = _rand_pos(rng, (65, 85), (25, 55))
        events.append(_make_run(idx, ts, pid, x, y, "decoy_run", match_id=match_id))
        idx += 1

    # 2. Diagonal runs (5 instances) — angle 30-70 degrees, ≥5m
    diag_timestamps = [240, 900, 1800, 3300, 4500]
    diag_players = [_p(p) for p in ["p003", "p001", "p002", "p003", "p001"]]
    for ts, pid in zip(diag_timestamps, diag_players):
        if _is_in_scenario(ts):
            ts += 40
        x, y = _rand_pos(rng, (60, 80), (28, 44))
        events.append(_make_run(idx, ts, pid, x, y, "diagonal_run", match_id=match_id))
        idx += 1

    # 3. Overlapping runs (5 instances) — LB/RB advancing beyond ball
    overlap_timestamps = [300, 1100, 1950, 3600, 4700]
    overlap_players = [_p(p) for p in ["p010", "p007", "p010", "p007", "p010"]]
    for ts, pid in zip(overlap_timestamps, overlap_players):
        if _is_in_scenario(ts):
            ts += 25
        x = 55.0 if pid in (_p("p010"),) else 52.0
        y = 60.0 if pid in (_p("p010"),) else 10.0
        events.append(_make_run(idx, ts, pid, x, y, "overlapping_run", match_id=match_id))
        idx += 1

    # 4. Free space movement (5 instances) — movement into open zone
    free_timestamps = [420, 1200, 2100, 3800, 5000]
    free_players = [_p(p) for p in ["p003", "p004", "p005", "p003", "p004"]]
    for ts, pid in zip(free_timestamps, free_players):
        if _is_in_scenario(ts):
            ts += 35
        x, y = _rand_pos(rng, (55, 80), (28, 44))
        events.append(_make_run(idx, ts, pid, x, y, "free_space_movement", match_id=match_id))
        idx += 1

    # 5. Defensive tracking (5 instances) — defender within 3m of attacker
    track_timestamps = [600, 1350, 2500, 3700, 5100]
    track_players = [_p(p) for p in ["p008", "p009", "p008", "p009", "p008"]]
    track_targets = [_p(p) for p in ["p012", "p013", "p014", "p012", "p013"]]
    for ts, tracker, target in zip(track_timestamps, track_players, track_targets):
        if _is_in_scenario(ts):
            ts += 20
        x, y = _rand_pos(rng, (30, 60), (24, 48))
        events.append({
            "event_id": _evt_id(idx),
            "match_id": match_id,
            "timestamp": round(ts, 1),
            "frame_id": f"frm-{int(ts):04d}",
            "event_type": "defensive_track",
            "player_id": tracker,
            "team_id": PLAYER_TEAM.get(tracker, "team-northvale-fc"),
            "location": {"x": x, "y": y},
            "metadata": {"tracking_player_id": target, "distance": round(rng.uniform(1.5, 3.0), 1)},
            "sequence_tags": [],
        })
        idx += 1

    # 6. Covering runs (5 instances) — player fills empty defensive zone
    cover_timestamps = [660, 1500, 2600, 3900, 5200]
    cover_players = [_p(p) for p in ["p006", "p005", "p006", "p005", "p006"]]
    for ts, pid in zip(cover_timestamps, cover_players):
        if _is_in_scenario(ts):
            ts += 30
        x, y = _rand_pos(rng, (38, 58), (28, 44))
        events.append({
            "event_id": _evt_id(idx),
            "match_id": match_id,
            "timestamp": round(ts, 1),
            "frame_id": f"frm-{int(ts):04d}",
            "event_type": "covering_run",
            "player_id": pid,
            "team_id": PLAYER_TEAM.get(pid, "team-northvale-fc"),
            "location": {"x": x, "y": y},
            "metadata": {"zone": "central_defensive", "trigger": "teammate_out_of_position"},
            "sequence_tags": [],
        })
        idx += 1

    # 7. Pressing movements (5 instances, beyond SEQ-003)
    press_timestamps = [750, 1650, 2700, 3200, 5300]
    press_players = [_p(p) for p in ["p004", "p005", "p004", "p006", "p005"]]
    press_targets = [_p(p) for p in ["p017", "p015", "p016", "p017", "p015"]]
    for ts, pid, tgt in zip(press_timestamps, press_players, press_targets):
        if _is_in_scenario(ts):
            ts += 28
        x, y = _rand_pos(rng, (50, 70), (26, 46))
        events.append(_make_press(idx, ts, pid, x, y, tgt, match_id=match_id))
        idx += 1

    # ── Phase 2: Filler events to reach ≥150 total ────────────────────────────

    # Regular passes — both teams
    pass_timestamps = list(range(60, 5400, 38))
    for ts in pass_timestamps:
        if _is_in_scenario(ts) or len(events) > 180:
            continue
        if ts % 2 == 0:
            pid = rng.choice(h_players[:-1])  # exclude GK
            team = "home"
        else:
            pid = rng.choice(a_players[:-1])
            team = "away"

        fx, fy = _rand_pos(rng, (20, 80), (10, 60))
        dx = rng.uniform(5, 20) * (1 if team == "home" else -1)
        dy = rng.uniform(-10, 10)
        tx = _clamp(fx + dx, 1, PITCH_W - 1)
        ty = _clamp(fy + dy, 1, PITCH_H - 1)
        outcome = "complete" if rng.random() < 0.78 else "incomplete"
        events.append(_make_pass(idx, ts, pid, fx, fy, tx, ty, match_id=match_id, outcome=outcome,
                                 pressure=rng.random() < 0.2, forward=(dx > 0)))
        idx += 1

    # Shots (12 shots across match)
    shot_ts = [510, 1080, 1620, 2160, 2880, 3240, 3780, 4050, 4620, 4860, 5040, 5280]
    shot_players = [_p(p) for p in ["p001", "p012", "p003", "p013", "p001", "p014", "p003", "p012", "p001", "p013", "p003", "p001"]]
    for ts, pid in zip(shot_ts, shot_players):
        if _is_in_scenario(ts):
            continue
        team = "home" if pid in h_players else "away"
        x = rng.uniform(80, 100) if team == "home" else rng.uniform(5, 25)
        y = rng.uniform(24, 44)
        on_target = rng.random() < 0.4
        events.append(_make_shot(idx, ts, pid, x, y, on_target, match_id=match_id))
        idx += 1

    # Tackles (10 tackles)
    tackle_ts = list(range(400, 5200, 480))
    for ts in tackle_ts[:10]:
        if _is_in_scenario(ts):
            ts += 15
        pid = rng.choice(h_players[5:10] + a_players[5:10])
        x, y = _rand_pos(rng, (25, 75), (15, 55))
        events.append(_make_tackle(idx, ts, pid, x, y, match_id=match_id))
        idx += 1

    # Direction changes (defender reactions, 10 more)
    for i in range(10):
        ts = 200 + i * 520
        if _is_in_scenario(ts):
            ts += 22
        pid = rng.choice(a_players[5:9])
        response = rng.choice(h_players[:5])
        x, y = _rand_pos(rng, (55, 80), (20, 50))
        events.append(_make_change_dir(idx, ts, pid, x, y, response, match_id=match_id))
        idx += 1

    # Sort by timestamp
    events.sort(key=lambda e: e["timestamp"])

    return events

    # Sort by timestamp
    events.sort(key=lambda e: e["timestamp"])

    return events
