"""Duration alert builder."""

from __future__ import annotations

def build_duration_alert(name: str, elapsed_seconds: float, level: str) -> dict:
    return {
        "name": name,
        "elapsed_seconds": elapsed_seconds,
        "level": level,
        "message": f"{name} collection took {elapsed_seconds:.3f}s",
    }

