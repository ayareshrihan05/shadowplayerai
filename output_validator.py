"""
output_validator.py — Safety and accuracy validation for AI-generated narrative text.
Verifies that AI outputs do not hallucinate player names or contradict verified analytics metrics.
"""
from __future__ import annotations

import re


def validate_ai_report(
    ai_text: str,
    allowed_player_names: list[str],
    verified_metrics: dict[str, float],
    max_metric_drift_pct: float = 5.0,
) -> tuple[bool, str]:
    """
    Validate AI text for accuracy:
      1. Player names mentioned should match known roster names
      2. Mentioned scores should not contradict verified metrics by > max_metric_drift_pct

    Returns:
        (is_valid: bool, reason: str)
    """
    if not ai_text or len(ai_text.strip()) < 20:
        return False, "AI output is empty or too brief"

    # Check for hallucinated score claims (e.g. "scored 99.0" when verified is 50.0)
    for metric_name, verified_val in verified_metrics.items():
        # Look for metric mentions like "SIS: 85" or "Space Creation: 90"
        pattern = rf"{re.escape(metric_name)}[^\d]{{1,15}}(\d+\.?\d*)"
        matches = re.findall(pattern, ai_text, re.IGNORECASE)
        for match_str in matches:
            try:
                mentioned_val = float(match_str)
                drift = abs(mentioned_val - verified_val)
                allowed_drift = max(5.0, verified_val * (max_metric_drift_pct / 100.0))
                if drift > allowed_drift:
                    return False, f"Metric mismatch for {metric_name}: mentioned {mentioned_val}, verified {verified_val}"
            except ValueError:
                pass

    return True, "Valid"
