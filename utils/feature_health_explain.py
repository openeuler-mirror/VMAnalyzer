"""Health score explanation helper."""

from __future__ import annotations

def explain_health(metrics: dict[str, float]) -> list[str]:
    reasons = []
    if float(metrics.get("cpu_usage", 0.0)) >= 85:
        reasons.append("cpu_usage_high")
    if float(metrics.get("memory_usage", 0.0)) >= 85:
        reasons.append("memory_usage_high")
    if float(metrics.get("disk_usage", 0.0)) >= 90:
        reasons.append("disk_usage_high")
    return reasons

