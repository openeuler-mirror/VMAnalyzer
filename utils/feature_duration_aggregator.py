"""Duration aggregation helpers."""

from __future__ import annotations

from typing import Iterable


def aggregate(values: Iterable[float]) -> dict:
    samples = list(values)
    if not samples:
        return {"count": 0, "min": 0.0, "max": 0.0, "avg": 0.0}
    return {
        "count": len(samples),
        "min": min(samples),
        "max": max(samples),
        "avg": sum(samples) / len(samples),
    }

