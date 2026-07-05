"""Health threshold helpers."""

from __future__ import annotations

DEFAULT_THRESHOLDS = {"warning": 75.0, "critical": 50.0}


def threshold_for(level: str, thresholds: dict[str, float] | None = None) -> float:
    return (thresholds or DEFAULT_THRESHOLDS).get(level, 0.0)

