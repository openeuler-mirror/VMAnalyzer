"""Risk tag builder."""

from __future__ import annotations

def build_risk_tags(metrics: dict[str, float]) -> list[str]:
    tags = []
    if float(metrics.get("cpu_usage", 0.0)) >= 85:
        tags.append("high_cpu")
    if float(metrics.get("memory_usage", 0.0)) >= 85:
        tags.append("high_memory")
    if float(metrics.get("disk_usage", 0.0)) >= 90:
        tags.append("high_disk")
    return tags

