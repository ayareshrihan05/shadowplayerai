"""
Pydantic models for AI Scouting Reports.
All data described is synthetic and fictional.
"""
from __future__ import annotations
from pydantic import BaseModel


class ReportSections(BaseModel):
    overview: str
    off_ball_strengths: str
    key_sequences: str
    defensive_contributions: str
    attacking_contributions: str
    improvement_areas: str
    limitations: str


class ScoutingReport(BaseModel):
    player_id: str
    player_name: str
    generation_method: str  # "ai_generated" | "fallback_template"
    sections: ReportSections
    referenced_metrics: dict[str, float]
    disclaimer: str = (
        "SYNTHETIC DATA. This report is based on fictional match data and "
        "experimental metrics. SIS is not an official football statistic."
    )
