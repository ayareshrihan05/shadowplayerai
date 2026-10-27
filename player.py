"""
Pydantic models for player-level data and Shadow Profiles.
All data described is synthetic and fictional.
"""
from __future__ import annotations
from pydantic import BaseModel, Field


class ConventionalStats(BaseModel):
    goals: int = 0
    assists: int = 0
    shots: int = 0
    passes_completed: int = 0


class SISBreakdown(BaseModel):
    space_creation_score: float = Field(ge=0.0, le=100.0)  # S
    passing_lane_score: float = Field(ge=0.0, le=100.0)     # P
    defensive_support_score: float = Field(ge=0.0, le=100.0)  # D
    chain_reaction_score: float = Field(ge=0.0, le=100.0)   # C
    sis: float = Field(ge=0.0, le=100.0)
    confidence: float = Field(ge=0.0, le=1.0)
    label: str = "EXPERIMENTAL METRIC — NOT AN OFFICIAL STATISTIC"


class SequenceSummary(BaseModel):
    sequence_id: str
    name: str
    timestamp_start: float
    timestamp_end: float
    movement_type: str
    sis_contribution: float
    confidence: float


class PlayerSummary(BaseModel):
    player_id: str
    name: str
    team_id: str
    position: str
    sis_breakdown: SISBreakdown


class ShadowProfile(BaseModel):
    player_id: str
    player_name: str
    team_id: str
    position: str
    match_id: str
    minutes_played: int
    conventional_stats: ConventionalStats
    sis_breakdown: SISBreakdown
    top_sequences: list[SequenceSummary]
    strengths: list[str]
    potential_weaknesses: list[str]
    evidence_coverage: float = Field(ge=0.0, le=1.0)
    data_label: str = "SYNTHETIC DATA — FICTIONAL PLAYER"
