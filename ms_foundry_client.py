"""
ms_foundry_client.py — Microsoft Foundry / Azure AI endpoint client.
Gracefully handles absent credentials and network errors by returning None,
which triggers the deterministic fallback generator.
"""
from __future__ import annotations

import logging
import os
from typing import Any

import httpx

logger = logging.getLogger("shadowplayer.ai")

FOUNDRY_ENDPOINT = os.getenv("MS_FOUNDRY_ENDPOINT", "")
FOUNDRY_API_KEY = os.getenv("MS_FOUNDRY_API_KEY", "")
FOUNDRY_MODEL = os.getenv("MS_FOUNDRY_MODEL_NAME", "gpt-4o")
AI_FALLBACK_MODE = os.getenv("AI_FALLBACK_MODE", "true").lower() in ("true", "1", "yes")


async def call_foundry(prompt: str, system_prompt: str = "") -> str | None:
    """
    Invoke Microsoft Foundry model endpoint.
    Returns generated response text on success, or None on any error / missing config.
    """
    if AI_FALLBACK_MODE:
        logger.info("AI_FALLBACK_MODE is active — skipping Foundry call.")
        return None

    if not FOUNDRY_ENDPOINT or not FOUNDRY_API_KEY:
        logger.warning("Foundry endpoint or API key not configured — using fallback.")
        return None

    headers = {
        "Content-Type": "application/json",
        "api-key": FOUNDRY_API_KEY,
        "Authorization": f"Bearer {FOUNDRY_API_KEY}",
    }

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "messages": messages,
        "model": FOUNDRY_MODEL,
        "max_tokens": 1000,
        "temperature": 0.2,
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(FOUNDRY_ENDPOINT, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            choices = data.get("choices", [])
            if choices:
                return choices[0]["message"]["content"]
            return None
    except Exception as exc:
        logger.warning("Foundry API call failed: %s — falling back to deterministic template.", exc)
        return None
