"""Health score levels."""

from __future__ import annotations

def health_level(score: float) -> str:
    if score < 50:
        return "critical"
    if score < 75:
        return "warning"
    return "healthy"

