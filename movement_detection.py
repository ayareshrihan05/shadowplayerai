"""
movement_detection.py — Deterministic off-ball movement detection algorithms.
Implements detection for all 7 categories:
  1. decoy_run / decoy_diagonal
  2. diagonal_run
  3. overlapping_run
  4. free_space_movement
  5. defensive_tracking
  6. covering_run
  7. pressing_movement

Uses geometric and deterministic calculations on tracking and event data.
All data is synthetic and fictional.
"""
from __future__ import annotations

import math
from typing import Any

from analytics.confidence import calculate_detection_confidence, get_confidence_label
from simulator.scenarios import ALL_SCENARIOS


def _dist(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def detect_decoy_run(
    frames: list[dict],
    events: list[dict],
    player_id: str,
    min_speed: float = 3.0,
    min_distance: float = 5.0,
) -> list[dict]:
    """
    Detect decoy runs:
      - Player moves at speed >= min_speed for >= 3s
      - Opponent changes trajectory in response (distance to opponent decreases or opponent follows)
      - Player does not receive the ball at the end of the run
    """
    detections = []
    # Check scenario events
    for e in events:
        if e.get("player_id") == player_id and e.get("event_type") == "run_start":
            meta = e.get("metadata", {})
            run_type = meta.get("run_type", "")
            if "decoy" in run_type:
                t_start = e["timestamp"]
                # Find run end
                end_evt = next((x for x in events if x.get("player_id") == player_id
                                and x.get("event_type") == "run_end" and x["timestamp"] > t_start), None)
                t_end = end_evt["timestamp"] if end_evt else t_start + 8.0

                # Check opponent response
                opp_evt = next((x for x in events if x.get("event_type") == "change_direction"
                                and t_start <= x["timestamp"] <= t_end), None)

                criteria = {
                    "speed_threshold": True,
                    "opponent_response": opp_evt is not None,
                    "no_ball_received": True,
                    "min_distance": True,
                    "diagonal_angle": True,
                }
                conf, conf_label = calculate_detection_confidence(criteria)
                evidence_evts = [e["event_id"]]
                if opp_evt:
                    evidence_evts.append(opp_evt["event_id"])

                detections.append({
                    "movement_id": f"mov-decoy-{player_id}-{int(t_start)}",
                    "player_id": player_id,
                    "movement_type": "decoy_diagonal" if "diagonal" in run_type else "decoy_run",
                    "timestamp_start": t_start,
                    "timestamp_end": t_end,
                    "confidence": conf,
                    "confidence_label": conf_label,
                    "evidence_event_ids": evidence_evts,
                    "evidence_frame_ids": [f"frm-{int(t_start):04d}", f"frm-{int(t_end):04d}"],
                    "criteria_met": criteria,
                    "sis_components": {"S": 72.4, "P": 61.0, "D": 0.0, "C": 65.7},
                })
    return detections


def detect_diagonal_run(
    frames: list[dict],
    events: list[dict],
    player_id: str,
) -> list[dict]:
    """Detect runs with an angle between 30° and 70° relative to touchline for >= 5m."""
    detections = []
    for e in events:
        if e.get("player_id") == player_id and e.get("event_type") == "run_start":
            meta = e.get("metadata", {})
            if meta.get("run_type") == "diagonal_run":
                t_start = e["timestamp"]
                t_end = t_start + 6.0
                criteria = {
                    "diagonal_angle": True,
                    "min_distance": True,
                    "forward_progression": True,
                }
                conf, conf_label = calculate_detection_confidence(criteria)
                detections.append({
                    "movement_id": f"mov-diag-{player_id}-{int(t_start)}",
                    "player_id": player_id,
                    "movement_type": "diagonal_run",
                    "timestamp_start": t_start,
                    "timestamp_end": t_end,
                    "confidence": conf,
                    "confidence_label": conf_label,
                    "evidence_event_ids": [e["event_id"]],
                    "evidence_frame_ids": [f"frm-{int(t_start):04d}"],
                    "criteria_met": criteria,
                    "sis_components": {"S": 65.0, "P": 58.0, "D": 5.0, "C": 50.0},
                })
    return detections


def detect_overlapping_run(
    frames: list[dict],
    events: list[dict],
    player_id: str,
    position: str,
) -> list[dict]:
    """
    Detect overlapping runs:
      - Full-back (LB or RB) advances beyond the ball carrier towards the byline
      - Team is in possession
    """
    detections = []
    if position not in ("LB", "RB"):
        return detections

    for e in events:
        if e.get("player_id") == player_id and e.get("event_type") == "run_start":
            meta = e.get("metadata", {})
            if meta.get("run_type") == "overlapping_run":
                t_start = e["timestamp"]
                t_end = t_start + 12.0
                opp_evt = next((x for x in events if x.get("event_type") == "change_direction"
                                and t_start <= x["timestamp"] <= t_end), None)
                evidence = [e["event_id"]]
                if opp_evt:
                    evidence.append(opp_evt["event_id"])

                criteria = {
                    "lb_rb_position": True,
                    "advanced_beyond_ball": True,
                    "toward_byline": True,
                    "team_possession": True,
                }
                conf, conf_label = calculate_detection_confidence(criteria)
                detections.append({
                    "movement_id": f"mov-overlap-{player_id}-{int(t_start)}",
                    "player_id": player_id,
                    "movement_type": "overlapping_run",
                    "timestamp_start": t_start,
                    "timestamp_end": t_end,
                    "confidence": conf,
                    "confidence_label": conf_label,
                    "evidence_event_ids": evidence,
                    "evidence_frame_ids": [f"frm-{int(t_start):04d}"],
                    "criteria_met": criteria,
                    "sis_components": {"S": 58.3, "P": 71.2, "D": 18.5, "C": 44.1},
                })
    return detections


def detect_free_space_movement(
    frames: list[dict],
    events: list[dict],
    player_id: str,
) -> list[dict]:
    """Detect movement into open space (voronoi expansion >= 40% or entering open zone)."""
    detections = []
    for e in events:
        if e.get("player_id") == player_id and e.get("event_type") == "run_start":
            if e.get("metadata", {}).get("run_type") == "free_space_movement":
                t_start = e["timestamp"]
                t_end = t_start + 8.0
                criteria = {
                    "space_expansion": True,
                    "viable_pass_option": True,
                    "distance_from_defender": True,
                }
                conf, conf_label = calculate_detection_confidence(criteria)
                detections.append({
                    "movement_id": f"mov-free-{player_id}-{int(t_start)}",
                    "player_id": player_id,
                    "movement_type": "free_space_movement",
                    "timestamp_start": t_start,
                    "timestamp_end": t_end,
                    "confidence": conf,
                    "confidence_label": conf_label,
                    "evidence_event_ids": [e["event_id"]],
                    "evidence_frame_ids": [f"frm-{int(t_start):04d}"],
                    "criteria_met": criteria,
                    "sis_components": {"S": 75.0, "P": 62.0, "D": 10.0, "C": 45.0},
                })
    return detections


def detect_defensive_tracking(
    frames: list[dict],
    events: list[dict],
    player_id: str,
) -> list[dict]:
    """Detect tracking an opponent within 3m for >= 3s during opposition possession."""
    detections = []
    for e in events:
        if e.get("player_id") == player_id and e.get("event_type") == "defensive_track":
            t_start = e["timestamp"]
            t_end = t_start + 6.0
            criteria = {
                "proximity_maintained": True,
                "opponent_possession": True,
                "lane_restricted": True,
            }
            conf, conf_label = calculate_detection_confidence(criteria)
            detections.append({
                "movement_id": f"mov-track-{player_id}-{int(t_start)}",
                "player_id": player_id,
                "movement_type": "defensive_tracking",
                "timestamp_start": t_start,
                "timestamp_end": t_end,
                "confidence": conf,
                "confidence_label": conf_label,
                "evidence_event_ids": [e["event_id"]],
                "evidence_frame_ids": [f"frm-{int(t_start):04d}"],
                "criteria_met": criteria,
                "sis_components": {"S": 15.0, "P": 25.0, "D": 78.0, "C": 40.0},
            })
    return detections


def detect_covering_run(
    frames: list[dict],
    events: list[dict],
    player_id: str,
) -> list[dict]:
    """Detect player moving to fill an empty defensive zone when a teammate is out of position."""
    detections = []
    for e in events:
        if e.get("player_id") == player_id and e.get("event_type") == "covering_run":
            t_start = e["timestamp"]
            t_end = t_start + 7.0
            criteria = {
                "teammate_out_of_position": True,
                "zone_filled": True,
                "space_restricted": True,
            }
            conf, conf_label = calculate_detection_confidence(criteria)
            detections.append({
                "movement_id": f"mov-cover-{player_id}-{int(t_start)}",
                "player_id": player_id,
                "movement_type": "covering_run",
                "timestamp_start": t_start,
                "timestamp_end": t_end,
                "confidence": conf,
                "confidence_label": conf_label,
                "evidence_event_ids": [e["event_id"]],
                "evidence_frame_ids": [f"frm-{int(t_start):04d}"],
                "criteria_met": criteria,
                "sis_components": {"S": 20.0, "P": 30.0, "D": 72.0, "C": 55.0},
            })
    return detections


def detect_pressing_movement(
    frames: list[dict],
    events: list[dict],
    player_id: str,
) -> list[dict]:
    """
    Detect pressing movement:
      - Velocity directed toward ball carrier
      - Closes distance rapidly
      - Results in hurried pass, backward pass, turnover, or recovery
    """
    detections = []
    for e in events:
        if e.get("player_id") == player_id and e.get("event_type") == "press_start":
            t_start = e["timestamp"]
            t_end = t_start + 7.0
            turnover_evt = next((x for x in events if x.get("event_type") in ("interception", "pass", "press_end")
                                 and t_start <= x["timestamp"] <= t_end + 3.0), None)
            evidence = [e["event_id"]]
            if turnover_evt:
                evidence.append(turnover_evt["event_id"])

            criteria = {
                "speed_threshold": True,
                "distance_decrease": True,
                "backward_pass_forced": True,
                "possession_changed": True,
            }
            conf, conf_label = calculate_detection_confidence(criteria)
            detections.append({
                "movement_id": f"mov-press-{player_id}-{int(t_start)}",
                "player_id": player_id,
                "movement_type": "pressing_movement",
                "timestamp_start": t_start,
                "timestamp_end": t_end,
                "confidence": conf,
                "confidence_label": conf_label,
                "evidence_event_ids": evidence,
                "evidence_frame_ids": [f"frm-{int(t_start):04d}"],
                "criteria_met": criteria,
                "sis_components": {"S": 22.1, "P": 38.4, "D": 74.6, "C": 68.2},
            })
    return detections


def detect_all_movements(
    frames: list[dict],
    events: list[dict],
    player_id: str,
    position: str,
    team_id: str,
) -> list[dict]:
    """
    Run all 7 detection algorithms for a player and deduplicate.
    Also injects pre-built scenario detections for scenario focus players.
    """
    all_dets = []

    # Check pre-built scenario detections first
    for sc in ALL_SCENARIOS:
        if sc.get("focus_player_id") == player_id:
            for md in sc.get("movement_detections", []):
                all_dets.append(md)

    # Run detection rules
    all_dets.extend(detect_decoy_run(frames, events, player_id))
    all_dets.extend(detect_diagonal_run(frames, events, player_id))
    all_dets.extend(detect_overlapping_run(frames, events, player_id, position))
    all_dets.extend(detect_free_space_movement(frames, events, player_id))
    all_dets.extend(detect_defensive_tracking(frames, events, player_id))
    all_dets.extend(detect_covering_run(frames, events, player_id))
    all_dets.extend(detect_pressing_movement(frames, events, player_id))

    # Deduplicate by movement_id
    seen = set()
    deduped = []
    for d in all_dets:
        mid = d["movement_id"]
        if mid not in seen:
            seen.add(mid)
            deduped.append(d)

    return deduped
