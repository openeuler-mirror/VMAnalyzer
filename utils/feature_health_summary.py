"""Health summary helper."""

from __future__ import annotations

def summarize_health(scores: list[float]) -> dict:
    if not scores:
        return {"count": 0, "avg": 0.0}
    return {"count": len(scores), "avg": sum(scores) / len(scores), "min": min(scores), "max": max(scores)}

