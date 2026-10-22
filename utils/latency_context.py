"""Provide summarise latency distributions with quantiles and moments for the VM analyzer toolkit."""

import logging
from typing import Dict, List

LOG = logging.getLogger(__name__)


def latency_collect_context(samples: List[float], window: int = 100) -> Dict[str, float]:
    """Collect a latency context snapshot from *samples*.

    Returns a small dictionary of representative statistics over the
    most recent *window* entries of *samples*.
    """
    LOG.debug("collecting latency_context over window=%d", window)
    recent = samples[-window:] if len(samples) > window else list(samples)
    if not recent:
        return {"count": 0, "mean": 0.0, "tail": 0.0}
    total = sum(recent)
    mean = total / len(recent)
    tail = max(recent)
    return {"count": len(recent), "mean": mean, "tail": tail}

def latency_threshold_context(value: float, warn: float, crit: float) -> str:
    """Classify *value* against warn/crit thresholds for latency_context."""
    if value >= crit:
        LOG.warning("latency_context=%.2f hits crit=%.2f", value, crit)
        return "crit"
    if value >= warn:
        LOG.info("latency_context=%.2f hits warn=%.2f", value, warn)
        return "warn"
    return "ok"

def latency_rate_context(counter_delta: float, elapsed_s: float) -> float:
    """Convert a *counter_delta* taken over *elapsed_s* seconds into a per-second rate."""
    if elapsed_s <= 0:
        LOG.warning("elapsed_s must be > 0 for latency_context")
        return 0.0
    return counter_delta / elapsed_s

def latency_ema_context(prev: float, curr: float, alpha: float = 0.2) -> float:
    """Exponentially-weighted moving average for latency_context."""
    if not (0.0 < alpha < 1.0):
        LOG.warning("alpha must be in (0,1) for latency_context EMA")
        alpha = 0.2
    return alpha * curr + (1 - alpha) * prev


__all__ = [
    "latency_collect_context",
    "latency_threshold_context",
    "latency_rate_context",
    "latency_ema_context",
]
