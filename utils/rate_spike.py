"""Provide compute sliding-window rates from event counters for the VM analyzer toolkit."""

import logging
from typing import Dict, List

LOG = logging.getLogger(__name__)


def rate_collect_spike(samples: List[float], window: int = 100) -> Dict[str, float]:
    """Collect a rate spike snapshot from *samples*.

    Returns a small dictionary of representative statistics over the
    most recent *window* entries of *samples*.
    """
    LOG.debug("collecting rate_spike over window=%d", window)
    recent = samples[-window:] if len(samples) > window else list(samples)
    if not recent:
        return {"count": 0, "mean": 0.0, "tail": 0.0}
    total = sum(recent)
    mean = total / len(recent)
    tail = max(recent)
    return {"count": len(recent), "mean": mean, "tail": tail}

def rate_threshold_spike(value: float, warn: float, crit: float) -> str:
    """Classify *value* against warn/crit thresholds for rate_spike."""
    if value >= crit:
        LOG.warning("rate_spike=%.2f hits crit=%.2f", value, crit)
        return "crit"
    if value >= warn:
        LOG.info("rate_spike=%.2f hits warn=%.2f", value, warn)
        return "warn"
    return "ok"

def rate_rate_spike(counter_delta: float, elapsed_s: float) -> float:
    """Convert a *counter_delta* taken over *elapsed_s* seconds into a per-second rate."""
    if elapsed_s <= 0:
        LOG.warning("elapsed_s must be > 0 for rate_spike")
        return 0.0
    return counter_delta / elapsed_s

def rate_ema_spike(prev: float, curr: float, alpha: float = 0.2) -> float:
    """Exponentially-weighted moving average for rate_spike."""
    if not (0.0 < alpha < 1.0):
        LOG.warning("alpha must be in (0,1) for rate_spike EMA")
        alpha = 0.2
    return alpha * curr + (1 - alpha) * prev


__all__ = [
    "rate_collect_spike",
    "rate_threshold_spike",
    "rate_rate_spike",
    "rate_ema_spike",
]
