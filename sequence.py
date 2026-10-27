"""
Pydantic models for sequence and movement detection data.
All data described is synthetic and fictional.
"""
from __future__ import annotations
from pydantic import BaseModel, Field
from models.match import FrameData


class MovementDetection(BaseModel):
    movement_id: str
    player_id: str
    movement_type: str
    timestamp_start: float
    timestamp_end: float
    confidence: float = Field(ge=0.0, le=1.0)
    confidence_label: str  # "high" | "medium" | "low"
    evidence_event_ids: list[str]
    evidence_frame_ids: list[str]
    criteria_met: dict[str, bool]
    sis_components: dict[str, float]  # {"S": 72.4, "P": 61.0, "D": 0.0, "C": 65.7}


class AIExplanation(BaseModel):
    text: str
    evidence_refs: list[str]
    generation_method: str  # "ai_generated" | "fallback_template"
    disclaimer: str = (
        "This explanation is based on synthetic data and experimental metrics. "
        "All players and events are fictional."
    )


class SequenceDetail(BaseModel):
    sequence_id: str
    name: str
    match_id: str
    focus_player_id: str
    timestamp_start: float
    timestamp_end: float
    frames: list[FrameData]
    key_events: list[str]
    movement_detections: list[MovementDetection]
    ai_explanation: AIExplanation
