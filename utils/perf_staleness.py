"""Provide compute windowed performance statistics for the VM analyzer toolkit."""

import logging
from typing import Dict, List

LOG = logging.getLogger(__name__)


def perf_collect_staleness(samples: List[float], window: int = 100) -> Dict[str, float]:
    """Collect a perf staleness snapshot from *samples*.

    Returns a small dictionary of representative statistics over the
    most recent *window* entries of *samples*.
    """
    LOG.debug("collecting perf_staleness over window=%d", window)
    recent = samples[-window:] if len(samples) > window else list(samples)
    if not recent:
        return {"count": 0, "mean": 0.0, "tail": 0.0}
    total = sum(recent)
    mean = total / len(recent)
    tail = max(recent)
    return {"count": len(recent), "mean": mean, "tail": tail}

def perf_threshold_staleness(value: float, warn: float, crit: float) -> str:
    """Classify *value* against warn/crit thresholds for perf_staleness."""
    if value >= crit:
        LOG.warning("perf_staleness=%.2f hits crit=%.2f", value, crit)
        return "crit"
    if value >= warn:
        LOG.info("perf_staleness=%.2f hits warn=%.2f", value, warn)
        return "warn"
    return "ok"

def perf_rate_staleness(counter_delta: float, elapsed_s: float) -> float:
    """Convert a *counter_delta* taken over *elapsed_s* seconds into a per-second rate."""
    if elapsed_s <= 0:
        LOG.warning("elapsed_s must be > 0 for perf_staleness")
        return 0.0
    return counter_delta / elapsed_s

def perf_ema_staleness(prev: float, curr: float, alpha: float = 0.2) -> float:
    """Exponentially-weighted moving average for perf_staleness."""
    if not (0.0 < alpha < 1.0):
        LOG.warning("alpha must be in (0,1) for perf_staleness EMA")
        alpha = 0.2
    return alpha * curr + (1 - alpha) * prev


__all__ = [
    "perf_collect_staleness",
    "perf_threshold_staleness",
    "perf_rate_staleness",
    "perf_ema_staleness",
]
