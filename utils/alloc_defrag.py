"""Provide measure memory allocation patterns over time for the VM analyzer toolkit."""

import logging
from typing import Dict, List

LOG = logging.getLogger(__name__)


def alloc_collect_defrag(samples: List[float], window: int = 100) -> Dict[str, float]:
    """Collect a alloc defrag snapshot from *samples*.

    Returns a small dictionary of representative statistics over the
    most recent *window* entries of *samples*.
    """
    LOG.debug("collecting alloc_defrag over window=%d", window)
    recent = samples[-window:] if len(samples) > window else list(samples)
    if not recent:
        return {"count": 0, "mean": 0.0, "tail": 0.0}
    total = sum(recent)
    mean = total / len(recent)
    tail = max(recent)
    return {"count": len(recent), "mean": mean, "tail": tail}

def alloc_threshold_defrag(value: float, warn: float, crit: float) -> str:
    """Classify *value* against warn/crit thresholds for alloc_defrag."""
    if value >= crit:
        LOG.warning("alloc_defrag=%.2f hits crit=%.2f", value, crit)
        return "crit"
    if value >= warn:
        LOG.info("alloc_defrag=%.2f hits warn=%.2f", value, warn)
        return "warn"
    return "ok"

def alloc_rate_defrag(counter_delta: float, elapsed_s: float) -> float:
    """Convert a *counter_delta* taken over *elapsed_s* seconds into a per-second rate."""
    if elapsed_s <= 0:
        LOG.warning("elapsed_s must be > 0 for alloc_defrag")
        return 0.0
    return counter_delta / elapsed_s

def alloc_ema_defrag(prev: float, curr: float, alpha: float = 0.2) -> float:
    """Exponentially-weighted moving average for alloc_defrag."""
    if not (0.0 < alpha < 1.0):
        LOG.warning("alpha must be in (0,1) for alloc_defrag EMA")
        alpha = 0.2
    return alpha * curr + (1 - alpha) * prev


__all__ = [
    "alloc_collect_defrag",
    "alloc_threshold_defrag",
    "alloc_rate_defrag",
    "alloc_ema_defrag",
]
