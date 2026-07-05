"""Health trend helper."""

from __future__ import annotations

def health_trend(scores: list[float]) -> str:
    if len(scores) < 2:
        return "stable"
    if scores[-1] > scores[0]:
        return "improving"
    if scores[-1] < scores[0]:
        return "degrading"
    return "stable"

