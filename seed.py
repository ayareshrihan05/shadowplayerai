"""
seed.py — Database seeding script for ShadowPlayer AI.
Generates synthetic match data for two gender-segregated matches:
  - match-men-001: Men's Premier League (Northvale FC vs Eastmere City)
  - match-women-001: Women's Super League (Northvale FC Women vs Eastmere City Women)
  - match-alpha-001: Compatibility alias for test suite

All data is synthetic and fictional.
"""
from __future__ import annotations

import copy
import logging
import os

from simulator.match_generator import generate_match
from simulator.scenarios import (
    MEN_HOME_TEAM, MEN_AWAY_TEAM, MEN_ALL_PLAYERS, MEN_SCENARIOS,
    WOMEN_HOME_TEAM, WOMEN_AWAY_TEAM, WOMEN_ALL_PLAYERS, WOMEN_SCENARIOS,
    ALL_SCENARIOS,
)
from analytics.movement_detection import detect_all_movements
from analytics.sis_calculator import calculate_sis_for_all_players
from counterfactual.simulator import simulate_counterfactual
from database.db import (
    init_db,
    save_match,
    save_events,
    save_sequence,
    save_player_analytics,
    save_counterfactual,
    populate_cache,
)

logger = logging.getLogger("shadowplayer.seed")

# Realistic conventional stats for synthetic players
CONVENTIONAL_STATS_MAP: dict[str, dict] = {
    # Men's Squad
    "p001": {"goals": 1, "assists": 0, "shots": 3, "passes_completed": 14},  # Holloway ST
    "p002": {"goals": 0, "assists": 1, "shots": 2, "passes_completed": 22},  # Sterling LW
    "p003": {"goals": 1, "assists": 1, "shots": 4, "passes_completed": 38},  # Reeves CAM
    "p004": {"goals": 0, "assists": 0, "shots": 1, "passes_completed": 45},  # Ayo CM
    "p005": {"goals": 0, "assists": 0, "shots": 1, "passes_completed": 42},  # Briggs CM
    "p006": {"goals": 0, "assists": 0, "shots": 0, "passes_completed": 51},  # Laine DM
    "p007": {"goals": 0, "assists": 0, "shots": 0, "passes_completed": 34},  # Davies RB
    "p008": {"goals": 0, "assists": 0, "shots": 0, "passes_completed": 48},  # Kapoor CB
    "p009": {"goals": 0, "assists": 1, "shots": 0, "passes_completed": 54},  # Wright CB
    "p010": {"goals": 0, "assists": 1, "shots": 1, "passes_completed": 36},  # Cole LB
    "p011": {"goals": 0, "assists": 0, "shots": 0, "passes_completed": 18},  # Webb GK
    "p012": {"goals": 1, "assists": 0, "shots": 2, "passes_completed": 11},  # Hollis ST
    "p013": {"goals": 0, "assists": 0, "shots": 2, "passes_completed": 19},  # Vance RW
    "p014": {"goals": 0, "assists": 1, "shots": 2, "passes_completed": 33},  # Osei CAM
    "p015": {"goals": 0, "assists": 0, "shots": 1, "passes_completed": 39},  # Mercer CM
    "p016": {"goals": 0, "assists": 0, "shots": 0, "passes_completed": 41},  # Johansson CM
    "p017": {"goals": 0, "assists": 0, "shots": 0, "passes_completed": 37},  # Aluko DM
    "p018": {"goals": 0, "assists": 0, "shots": 0, "passes_completed": 28},  # Brandt RB
    "p019": {"goals": 0, "assists": 0, "shots": 0, "passes_completed": 44},  # Fitzpatrick CB
    "p020": {"goals": 0, "assists": 0, "shots": 0, "passes_completed": 40},  # Asante CB
    "p021": {"goals": 0, "assists": 0, "shots": 0, "passes_completed": 26},  # Kelly LB
    "p022": {"goals": 0, "assists": 0, "shots": 0, "passes_completed": 16},  # Drummond GK
    # Women's Squad
    "w001": {"goals": 1, "assists": 0, "shots": 3, "passes_completed": 16},  # Lindqvist ST
    "w002": {"goals": 0, "assists": 1, "shots": 2, "passes_completed": 24},  # Okonkwo LW
    "w003": {"goals": 1, "assists": 1, "shots": 4, "passes_completed": 40},  # Vasquez CAM
    "w004": {"goals": 0, "assists": 0, "shots": 1, "passes_completed": 47},  # Walsh-Sloan CM
    "w005": {"goals": 0, "assists": 0, "shots": 1, "passes_completed": 41},  # Brooks CM
    "w006": {"goals": 0, "assists": 0, "shots": 0, "passes_completed": 53},  # Diallo DM
    "w007": {"goals": 0, "assists": 0, "shots": 0, "passes_completed": 33},  # Ndiaye RB
    "w008": {"goals": 0, "assists": 0, "shots": 0, "passes_completed": 51},  # Williamson-Park CB
    "w009": {"goals": 0, "assists": 1, "shots": 0, "passes_completed": 55},  # Torres CB
    "w010": {"goals": 0, "assists": 1, "shots": 1, "passes_completed": 38},  # Fernandez LB
    "w011": {"goals": 0, "assists": 0, "shots": 0, "passes_completed": 19},  # Hampton GK
    "w012": {"goals": 1, "assists": 0, "shots": 2, "passes_completed": 12},  # Mead-Kelly ST
    "w013": {"goals": 0, "assists": 0, "shots": 2, "passes_completed": 18},  # Menon RW
    "w014": {"goals": 0, "assists": 1, "shots": 2, "passes_completed": 31},  # Hanson CAM
    "w015": {"goals": 0, "assists": 0, "shots": 1, "passes_completed": 37},  # Chen CM
    "w016": {"goals": 0, "assists": 0, "shots": 0, "passes_completed": 43},  # Brightwell CM
    "w017": {"goals": 0, "assists": 0, "shots": 0, "passes_completed": 39},  # Ibe DM
    "w018": {"goals": 0, "assists": 0, "shots": 0, "passes_completed": 27},  # Vance RB
    "w019": {"goals": 0, "assists": 0, "shots": 0, "passes_completed": 46},  # Farsi CB
    "w020": {"goals": 0, "assists": 0, "shots": 0, "passes_completed": 39},  # Hemp-Davis CB
    "w021": {"goals": 0, "assists": 0, "shots": 0, "passes_completed": 25},  # Dupont LB
    "w022": {"goals": 0, "assists": 0, "shots": 0, "passes_completed": 17},  # Earps-Cole GK
}

PLAYER_STRENGTHS: dict[str, tuple[list[str], list[str]]] = {
    "p001": (
        ["Decoy running into half-spaces", "Pinning central defenders", "Creating central channels for midfielders"],
        ["Defensive pressing recovery rate", "Holding width when play shifts"],
    ),
    "p010": (
        ["High-tempo overlapping runs", "Creating width in final third", "Forcing opposition full-backs into isolation"],
        ["Tracking back during rapid turnovers", "Central corridor coverage"],
    ),
    "p004": (
        ["Aggressive central pressing triggers", "Disrupting forward passing lanes", "Second-ball anticipation"],
        ["Staying disciplined when isolated", "Over-committing on lateral presses"],
    ),
    "w002": (
        ["Blindside channel cutting", "Attracting central defenders away from box", "Creating half-space overload"],
        ["Defensive transition tracking", "Sustained wide pressing stamina"],
    ),
    "w010": (
        ["High-tempo overlapping runs", "Creating width in final third", "Forcing opposition full-backs into isolation"],
        ["Tracking back during rapid turnovers", "Central corridor coverage"],
    ),
    "w001": (
        ["Intelligent near-post runs", "Occupying dual centre-backs", "First-time layoff linkup"],
        ["Aerial duel contested win rate", "Holding ball against low blocks"],
    ),
}

DEFAULT_STRENGTHS = (
    ["Positional discipline in formation", "Supporting possession continuity"],
    ["Inconsistency during fast counter-attacks", "Late adjustment to diagonal overloads"],
)


def _seed_single_match(
    match_id: str,
    home_team: dict,
    away_team: dict,
    scenarios: list[dict],
    players: list[dict],
    seed_val: int = 42,
    duration: int = 5400,
    alias_match_id: str | None = None,
) -> None:
    logger.info("Generating match %s...", match_id)
    match_record = generate_match(
        match_id=match_id,
        seed=seed_val,
        duration_seconds=duration,
        home_team=home_team,
        away_team=away_team,
        scenarios=scenarios,
    )

    all_frames = match_record["frames"]
    all_events = match_record["events"]

    # 1. Detect off-ball movements
    logger.info("Detecting movements for %d players in %s...", len(players), match_id)
    all_detections: dict[str, list[dict]] = {}
    for p in players:
        pid = p["player_id"]
        pos = p["position"]
        tid = p["team_id"]
        dets = detect_all_movements(all_frames, all_events, pid, pos, tid)
        all_detections[pid] = dets

    # 2. Compute SIS
    logger.info("Computing SIS for %s...", match_id)
    sis_results = calculate_sis_for_all_players(players, all_detections)

    # 3. Update leaderboard
    leaderboard = []
    for p in players:
        pid = p["player_id"]
        sis_info = sis_results[pid]
        leaderboard.append({
            "player_id": pid,
            "name": p["name"],
            "position": p["position"],
            "sis": sis_info["sis"],
            "confidence": sis_info["confidence"],
        })
    leaderboard.sort(key=lambda x: x["sis"], reverse=True)
    match_record["sis_leaderboard"] = leaderboard

    # 4. Save match & events
    save_match(match_record)
    save_events(all_events)

    # Also save under alias if requested (e.g. match-alpha-001)
    if alias_match_id:
        alias_record = copy.deepcopy(match_record)
        alias_record["match_id"] = alias_match_id
        save_match(alias_record)
        alias_events = copy.deepcopy(all_events)
        for ev in alias_events:
            ev["event_id"] = f"alpha-{ev['event_id']}"
            ev["match_id"] = alias_match_id
        save_events(alias_events)

    # 5. Save player profiles
    target_matches = [match_id]
    if alias_match_id:
        target_matches.append(alias_match_id)

    for m_id in target_matches:
        for p in players:
            pid = p["player_id"]
            sis_info = sis_results[pid]
            conv_stats = CONVENTIONAL_STATS_MAP.get(pid, {"goals": 0, "assists": 0, "shots": 0, "passes_completed": 20})
            strengths, weaknesses = PLAYER_STRENGTHS.get(pid, DEFAULT_STRENGTHS)

            player_seq_summaries = []
            for det in all_detections.get(pid, [])[:3]:
                player_seq_summaries.append({
                    "sequence_id": det.get("movement_id", "seq-custom"),
                    "name": det.get("movement_type", "Tactical movement").replace("_", " ").title(),
                    "timestamp_start": det.get("timestamp_start", 0.0),
                    "timestamp_end": det.get("timestamp_end", 10.0),
                    "movement_type": det.get("movement_type", "off_ball_run"),
                    "sis_contribution": round(sis_info["sis"] * 0.4, 1),
                    "confidence": det.get("confidence", 0.75),
                })

            for sc in scenarios:
                if sc["focus_player_id"] == pid:
                    player_seq_summaries.insert(0, {
                        "sequence_id": sc["sequence_id"],
                        "name": sc["name"],
                        "timestamp_start": sc["timestamp_start"],
                        "timestamp_end": sc["timestamp_end"],
                        "movement_type": sc["movement_detections"][0]["movement_type"] if sc["movement_detections"] else "off_ball_run",
                        "sis_contribution": sis_info["sis"],
                        "confidence": sis_info["confidence"],
                    })

            profile = {
                "player_id": pid,
                "player_name": p["name"],
                "team_id": p["team_id"],
                "position": p["position"],
                "match_id": m_id,
                "minutes_played": 90,
                "conventional_stats": conv_stats,
                "sis_breakdown": sis_info,
                "top_sequences": player_seq_summaries[:4],
                "strengths": strengths,
                "potential_weaknesses": weaknesses,
                "evidence_coverage": 0.88 if pid in ("p001", "p010", "p004", "w002", "w010", "w001") else 0.72,
                "data_label": "SYNTHETIC DATA — FICTIONAL PLAYER",
            }

            save_player_analytics(
                player_id=pid,
                match_id=m_id,
                sis_data={
                    "sis": sis_info["sis"],
                    "S": sis_info["space_creation_score"],
                    "P": sis_info["passing_lane_score"],
                    "D": sis_info["defensive_support_score"],
                    "C": sis_info["chain_reaction_score"],
                    "confidence": sis_info["confidence"],
                },
                profile=profile,
            )


def run_seed() -> None:
    """Execute complete seed process for both Men's and Women's matches."""
    logger.info("Initializing database...")
    init_db()

    seed_val = int(os.getenv("MATCH_SEED", "42"))
    duration = int(os.getenv("MATCH_DURATION_SECONDS", "5400"))

    # Seed 1: Men's Match (Northvale FC vs Eastmere City) + match-alpha-001 alias
    _seed_single_match(
        match_id="match-men-001",
        home_team=MEN_HOME_TEAM,
        away_team=MEN_AWAY_TEAM,
        scenarios=MEN_SCENARIOS,
        players=MEN_ALL_PLAYERS,
        seed_val=seed_val,
        duration=duration,
        alias_match_id="match-alpha-001",
    )

    # Seed 2: Women's Match (Northvale FC Women vs Eastmere City Women)
    _seed_single_match(
        match_id="match-women-001",
        home_team=WOMEN_HOME_TEAM,
        away_team=WOMEN_AWAY_TEAM,
        scenarios=WOMEN_SCENARIOS,
        players=WOMEN_ALL_PLAYERS,
        seed_val=seed_val + 1,
        duration=duration,
        alias_match_id=None,
    )

    # Save all prebuilt sequences (SEQ-001, SEQ-002, SEQ-003, SEQ-004)
    logger.info("Saving %d tactical sequences...", len(ALL_SCENARIOS))
    for seq in ALL_SCENARIOS:
        save_sequence(seq)

    # Precompute and save counterfactuals for all scenarios
    logger.info("Computing and saving counterfactual simulations...")
    for sc in ALL_SCENARIOS:
        cf_result = simulate_counterfactual(sc, sc["focus_player_id"], cf_type="remove_movement")
        save_counterfactual(sc["sequence_id"], "remove_movement", cf_result)

    # Populate cache
    logger.info("Populating in-memory cache...")
    populate_cache()
    logger.info("Database seeding complete!")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_seed()
