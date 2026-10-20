"""Compute filesystem usage percentages and simple capacity thresholds."""


def usage_percent(total, used):
    """Return the used percentage in ``[0, 100]`` guarded against bad totals."""
    if total <= 0:
        return 0.0
    clamped = max(0, min(used, total))
    return round(clamped / total * 100.0, 2)


def usage_from_blocks(blocks, bfree, bavail):
    """Derive used percentage from ``df`` style block counters."""
    used = max(0, blocks - bfree)
    return usage_percent(blocks, used)


def classify_usage(percent, warn=75.0, critical=90.0):
    """Classify a usage percentage into ``ok``, ``warn`` or ``critical``."""
    if percent >= critical:
        return "critical"
    if percent >= warn:
        return "warn"
    return "ok"


def remaining_bytes(total, used):
    """Return the number of free bytes, never below zero."""
    return max(0, total - used)


__all__ = ["usage_percent", "usage_from_blocks", "classify_usage", "remaining_bytes"]
