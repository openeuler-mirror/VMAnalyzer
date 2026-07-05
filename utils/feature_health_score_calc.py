"""Health score calculation."""

from __future__ import annotations

def clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def calculate_health_score(metrics: dict[str, float]) -> float:
    risk = (
        float(metrics.get("cpu_usage", 0.0)) * 0.25
        + float(metrics.get("memory_usage", 0.0)) * 0.25
        + float(metrics.get("disk_usage", 0.0)) * 0.2
        + float(metrics.get("error_count", 0.0)) * 0.3
    )
    return round(clamp(100.0 - risk), 2)

