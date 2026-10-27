"""
matches.py — Match overview, detail, player list, and tactical insights endpoints.
All data served is synthetic and fictional.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from api.dependencies import get_match_cache, api_response, api_error

router = APIRouter()


@router.get("/matches")
def list_matches(cache: dict = Depends(get_match_cache)):
    """List all available synthetic matches."""
    return api_response(cache["matches"])


@router.get("/matches/{match_id}")
def get_match_detail(match_id: str, cache: dict = Depends(get_match_cache)):
    """Retrieve full details for a match, including SIS leaderboard and team summaries."""
    match_data = cache["match_detail"].get(match_id)
    if not match_data:
        raise api_error("NOT_FOUND", f"Match '{match_id}' not found")

    detail = {
        "match_id": match_data["match_id"],
        "home_team": match_data["home_team"],
        "away_team": match_data["away_team"],
        "duration_seconds": match_data["duration_seconds"],
        "event_count": match_data["event_count"],
        "frame_count": match_data["frame_count"],
        "scenario_count": match_data["scenario_count"],
        "sis_leaderboard": match_data["sis_leaderboard"],
    }
    return api_response(detail)


@router.get("/matches/{match_id}/players")
def get_match_players(match_id: str, cache: dict = Depends(get_match_cache)):
    """Return all 22 players with their SIS breakdowns for this match."""
    match_data = cache["match_detail"].get(match_id)
    if not match_data:
        raise api_error("NOT_FOUND", f"Match '{match_id}' not found")

    players_list = []
    for (pid, mid), profile in cache["profiles"].items():
        if mid == match_id:
            players_list.append({
                "player_id": profile["player_id"],
                "name": profile["player_name"],
                "team_id": profile["team_id"],
                "position": profile["position"],
                "sis_breakdown": profile["sis_breakdown"],
            })

    return api_response(players_list)


@router.get("/matches/{match_id}/insights")
def get_match_insights(match_id: str, cache: dict = Depends(get_match_cache)):
    """Return top off-ball contributors, notable sequences, and team SIS comparisons."""
    match_data = cache["match_detail"].get(match_id)
    if not match_data:
        raise api_error("NOT_FOUND", f"Match '{match_id}' not found")

    leaderboard = match_data.get("sis_leaderboard", [])
    top_contributors = leaderboard[:5]

    notable_seqs = []
    for seq_id, seq in cache["sequences"].items():
        seq_mid = seq.get("match_id")
        if seq_mid and seq_mid != match_id and match_id != "match-alpha-001":
            continue
        notable_seqs.append({
            "sequence_id": seq["sequence_id"],
            "name": seq["name"],
            "focus_player_id": seq["focus_player_id"],
            "timestamp_start": seq["timestamp_start"],
            "timestamp_end": seq["timestamp_end"],
            "ai_summary": seq.get("ai_explanation", {}).get("text", "")[:120] + "...",
        })

    # Team SIS averages
    home_id = match_data["home_team"]["team_id"]
    away_id = match_data["away_team"]["team_id"]
    home_profiles = [p for (pid, mid), p in cache["profiles"].items() if mid == match_id and p["team_id"] == home_id]
    away_profiles = [p for (pid, mid), p in cache["profiles"].items() if mid == match_id and p["team_id"] == away_id]
    
    home_sis = [p["sis_breakdown"]["sis"] for p in home_profiles]
    away_sis = [p["sis_breakdown"]["sis"] for p in away_profiles]

    home_avg = round(sum(home_sis) / len(home_sis), 1) if home_sis else 50.0
    away_avg = round(sum(away_sis) / len(away_sis), 1) if away_sis else 50.0

    top_home = max(home_profiles, key=lambda p: p["sis_breakdown"]["sis"], default=None)
    top_away = max(away_profiles, key=lambda p: p["sis_breakdown"]["sis"], default=None)

    insights = {
        "match_id": match_id,
        "top_off_ball_contributors": top_contributors,
        "notable_sequences": notable_seqs,
        "team_sis_summary": {
            home_id: {
                "avg_sis": home_avg,
                "top_player": top_home["player_name"] if top_home else "N/A",
            },
            away_id: {
                "avg_sis": away_avg,
                "top_player": top_away["player_name"] if top_away else "N/A",
            },
        },
    }
    return api_response(insights)
