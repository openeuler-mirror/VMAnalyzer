"""Error summary formatter."""

from __future__ import annotations

def format_error_summary(counts: dict[str, int]) -> str:
    if not counts:
        return "No collection errors"
    return ", ".join(f"{name}={count}" for name, count in sorted(counts.items()))

