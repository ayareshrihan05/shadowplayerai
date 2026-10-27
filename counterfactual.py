"""
Pydantic models for counterfactual simulation results.
All data described is synthetic and fictional.
"""
from __future__ import annotations
from pydantic import BaseModel
from models.match import FrameData


class ScenarioMetrics(BaseModel):
    space_created_m2: float
    passing_lanes_available: int
    defensive_coverage_pct: float
    estimated_chance_quality: float


class ScenarioState(BaseModel):
    frames: list[FrameData]
    metrics: ScenarioMetrics


class CounterfactualDelta(BaseModel):
    delta_space_m2: float
    delta_passing_lanes: int
    delta_defensive_coverage_pct: float
    delta_chance_quality: float


class CounterfactualResult(BaseModel):
    sequence_id: str
    counterfactual_type: str
    observed: ScenarioState
    counterfactual: ScenarioState
    delta: CounterfactualDelta
    label: str = "SIMULATED COUNTERFACTUAL — NOT A REAL OUTCOME"
