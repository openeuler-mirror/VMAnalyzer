"""Duration threshold evaluator."""

from __future__ import annotations

def classify_duration(elapsed_seconds: float, warn_seconds: float = 2.0, critical_seconds: float = 5.0) -> str:
    if elapsed_seconds >= critical_seconds:
        return "critical"
    if elapsed_seconds >= warn_seconds:
        return "warning"
    return "ok"

