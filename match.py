"""
Pydantic models for match-level data.
These are the API contracts — TypeScript types must mirror these exactly.
All data described is synthetic and fictional.
"""
from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, Field


class Location(BaseModel):
    x: float
    y: float


class BallState(BaseModel):
    x: float
    y: float
    vx: float
    vy: float
    z: float = 0.0
    speed: float


class PossessionState(BaseModel):
    team_id: str | None = None
    player_id: str | None = None
    phase: Literal["buildup", "attack", "transition", "setpiece", "defensive"] = "buildup"


class PlayerPosition(BaseModel):
    player_id: str
    x: float = Field(ge=0.0, le=105.0)
    y: float = Field(ge=0.0, le=68.0)
    vx: float = 0.0
    vy: float = 0.0
    speed: float = 0.0
    is_in_possession: bool = False


class PassingLane(BaseModel):
    from_player: str
    to_player: str
    blocked: bool
    width: float
    length: float


class OpenSpaceZone(BaseModel):
    x: float
    y: float
    radius: float


class FrameData(BaseModel):
    """Lightweight frame for sequence replay — subset of full tracking frame."""
    t: float
    players: list[PlayerPosition]
    ball: BallState
    passing_lanes: list[PassingLane] = []
    open_space_zones: list[OpenSpaceZone] = []


class PlayerRecord(BaseModel):
    player_id: str
    name: str
    team_id: str
    position: str
    jersey_number: int
    is_fictional: bool = True


class TeamRecord(BaseModel):
    team_id: str
    name: str
    formation: str
    players: list[PlayerRecord]


class SISLeaderboardEntry(BaseModel):
    player_id: str
    name: str
    position: str
    sis: float
    confidence: float


class MatchSummary(BaseModel):
    match_id: str
    home_team: TeamRecord
    away_team: TeamRecord
    duration_seconds: int
    generated_at: str
    data_label: str = "SYNTHETIC MATCH — FICTIONAL"


class MatchDetail(BaseModel):
    match_id: str
    home_team: TeamRecord
    away_team: TeamRecord
    duration_seconds: int
    event_count: int
    frame_count: int
    scenario_count: int
    sis_leaderboard: list[SISLeaderboardEntry]


class TeamSISSummary(BaseModel):
    avg_sis: float
    top_player: str


class MatchInsights(BaseModel):
    match_id: str
    top_off_ball_contributors: list[SISLeaderboardEntry]
    notable_sequences: list[dict]
    team_sis_summary: dict[str, TeamSISSummary]
