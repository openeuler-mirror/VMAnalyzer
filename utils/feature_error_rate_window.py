"""Error rate window helper."""

from __future__ import annotations

def error_rate(error_count: int, sample_count: int) -> float:
    if sample_count <= 0:
        return 0.0
    return error_count / sample_count

