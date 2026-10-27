"""
confidence.py — Confidence scoring and labels for off-ball movement detections.
All classifications are deterministic and rule-based.
"""
from __future__ import annotations


def get_confidence_label(score: float) -> str:
    """
    Return human-readable confidence label based on numeric score.
    High: >= 0.75
    Medium: >= 0.50
    Low: < 0.50
    """
    if score >= 0.75:
        return "high"
    elif score >= 0.50:
        return "medium"
    return "low"


def calculate_detection_confidence(
    criteria_met: dict[str, bool],
    data_quality_factor: float = 1.0,
) -> tuple[float, str]:
    """
    Calculate confidence based on proportion of criteria satisfied.

    Args:
        criteria_met: dict of criterion_name -> bool
        data_quality_factor: multiplier in [0.0, 1.0]

    Returns:
        (confidence_score: float, label: str)
    """
    if not criteria_met:
        return 0.0, "low"

    satisfied = sum(1 for v in criteria_met.values() if v)
    total = len(criteria_met)
    raw_confidence = satisfied / total

    # Scale with quality factor and clamp
    final_score = max(0.0, min(1.0, round(raw_confidence * data_quality_factor, 2)))
    label = get_confidence_label(final_score)

    return final_score, label
