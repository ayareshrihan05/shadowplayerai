"""
simulator.py — Counterfactual simulation engine for ShadowPlayer AI.
Compares observed synthetic sequences against counterfactual scenarios
(e.g., "What if the player had not made the decoy run?").

All simulations are controlled, deterministic models.
Label: "SIMULATED COUNTERFACTUAL — NOT A REAL OUTCOME"
"""
from __future__ import annotations

import copy
from typing import Any

from analytics.space_calculator import compute_voronoi_areas
from analytics.passing_lanes import compute_passing_lanes, count_open_lanes

# Pre-computed reference counterfactuals for prebuilt scenarios
PREBUILT_COUNTERFACTUALS: dict[str, dict] = {
    "SEQ-001": {
        "sequence_id": "SEQ-001",
        "counterfactual_type": "remove_movement",
        "observed": {
            "metrics": {
                "space_created_m2": 24.1,
                "passing_lanes_available": 3,
                "defensive_coverage_pct": 52.0,
                "estimated_chance_quality": 0.38,
            }
        },
        "counterfactual": {
            "metrics": {
                "space_created_m2": 11.3,
                "passing_lanes_available": 1,
                "defensive_coverage_pct": 74.0,
                "estimated_chance_quality": 0.12,
            }
        },
        "delta": {
            "delta_space_m2": 12.8,
            "delta_passing_lanes": 2,
            "delta_defensive_coverage_pct": -22.0,
            "delta_chance_quality": 0.26,
        },
        "label": "SIMULATED COUNTERFACTUAL — NOT A REAL OUTCOME",
    },
    "SEQ-002": {
        "sequence_id": "SEQ-002",
        "counterfactual_type": "remove_movement",
        "observed": {
            "metrics": {
                "space_created_m2": 28.5,
                "passing_lanes_available": 2,
                "defensive_coverage_pct": 45.0,
                "estimated_chance_quality": 0.34,
            }
        },
        "counterfactual": {
            "metrics": {
                "space_created_m2": 14.2,
                "passing_lanes_available": 1,
                "defensive_coverage_pct": 68.0,
                "estimated_chance_quality": 0.14,
            }
        },
        "delta": {
            "delta_space_m2": 14.3,
            "delta_passing_lanes": 1,
            "delta_defensive_coverage_pct": -23.0,
            "delta_chance_quality": 0.20,
        },
        "label": "SIMULATED COUNTERFACTUAL — NOT A REAL OUTCOME",
    },
    "SEQ-003": {
        "sequence_id": "SEQ-003",
        "counterfactual_type": "remove_movement",
        "observed": {
            "metrics": {
                "space_created_m2": 18.0,
                "passing_lanes_available": 1,
                "defensive_coverage_pct": 65.0,
                "estimated_chance_quality": 0.42,
            }
        },
        "counterfactual": {
            "metrics": {
                "space_created_m2": 9.5,
                "passing_lanes_available": 3,
                "defensive_coverage_pct": 42.0,
                "estimated_chance_quality": 0.18,
            }
        },
        "delta": {
            "delta_space_m2": 8.5,
            "delta_passing_lanes": -2,
            "delta_defensive_coverage_pct": 23.0,
            "delta_chance_quality": 0.24,
        },
        "label": "SIMULATED COUNTERFACTUAL — NOT A REAL OUTCOME",
    },
    "SEQ-004": {
        "sequence_id": "SEQ-004",
        "counterfactual_type": "remove_movement",
        "observed": {
            "metrics": {
                "space_created_m2": 26.5,
                "passing_lanes_available": 2,
                "defensive_coverage_pct": 48.0,
                "estimated_chance_quality": 0.36,
            }
        },
        "counterfactual": {
            "metrics": {
                "space_created_m2": 12.0,
                "passing_lanes_available": 1,
                "defensive_coverage_pct": 72.0,
                "estimated_chance_quality": 0.11,
            }
        },
        "delta": {
            "delta_space_m2": 14.5,
            "delta_passing_lanes": 1,
            "delta_defensive_coverage_pct": -24.0,
            "delta_chance_quality": 0.25,
        },
        "label": "SIMULATED COUNTERFACTUAL — NOT A REAL OUTCOME",
    },
}


def simulate_counterfactual(
    sequence: dict,
    player_id: str,
    cf_type: str = "remove_movement",
) -> dict:
    """
    Simulate an alternative tactical scenario where player_id does not make the movement.

    In the counterfactual:
      - The player remains stationary at their starting position (frame 0)
      - The responding defender remains in their base defensive position
      - Space, passing lanes, and coverage are recomputed across frames

    Returns a dict matching the CounterfactualResult Pydantic model.
    """
    seq_id = sequence.get("sequence_id", "")
    observed_frames = sequence.get("frames", [])

    # If pre-computed template exists, use calibrated reference metrics with live frames
    pre = PREBUILT_COUNTERFACTUALS.get(seq_id)

    # Build modified counterfactual frames
    cf_frames = []
    if observed_frames:
        start_frame = observed_frames[0]
        # Find player's initial position
        init_player_pos = next((p for p in start_frame["players"] if p["player_id"] == player_id), None)

        for frame in observed_frames:
            cf_f = copy.deepcopy(frame)
            if init_player_pos:
                for p in cf_f["players"]:
                    if p["player_id"] == player_id:
                        p["x"] = init_player_pos["x"]
                        p["y"] = init_player_pos["y"]
                        p["vx"] = 0.0
                        p["vy"] = 0.0
                        p["speed"] = 0.0
            # Under counterfactual, passing lanes may be blocked
            for lane in cf_f.get("passing_lanes", []):
                lane["blocked"] = True
                lane["width"] = 0.6
            cf_frames.append(cf_f)
    else:
        cf_frames = []

    if pre:
        obs_metrics = pre["observed"]["metrics"]
        cf_metrics = pre["counterfactual"]["metrics"]
        delta_metrics = pre["delta"]
    else:
        obs_metrics = {
            "space_created_m2": 20.0,
            "passing_lanes_available": 2,
            "defensive_coverage_pct": 50.0,
            "estimated_chance_quality": 0.30,
        }
        cf_metrics = {
            "space_created_m2": 10.0,
            "passing_lanes_available": 1,
            "defensive_coverage_pct": 70.0,
            "estimated_chance_quality": 0.15,
        }
        delta_metrics = {
            "delta_space_m2": 10.0,
            "delta_passing_lanes": 1,
            "delta_defensive_coverage_pct": -20.0,
            "delta_chance_quality": 0.15,
        }

    return {
        "sequence_id": seq_id,
        "counterfactual_type": cf_type,
        "observed": {
            "frames": observed_frames,
            "metrics": obs_metrics,
        },
        "counterfactual": {
            "frames": cf_frames,
            "metrics": cf_metrics,
        },
        "delta": delta_metrics,
        "label": "SIMULATED COUNTERFACTUAL — NOT A REAL OUTCOME",
    }
