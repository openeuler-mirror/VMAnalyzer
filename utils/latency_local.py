"""Provide summarise latency distributions with quantiles and moments for the VM analyzer toolkit."""

import logging
from typing import Dict, List

LOG = logging.getLogger(__name__)


def latency_collect_local(samples: List[float], window: int = 100) -> Dict[str, float]:
    """Collect a latency local snapshot from *samples*.

    Returns a small dictionary of representative statistics over the
    most recent *window* entries of *samples*.
    """
    LOG.debug("collecting latency_local over window=%d", window)
    recent = samples[-window:] if len(samples) > window else list(samples)
    if not recent:
        return {"count": 0, "mean": 0.0, "tail": 0.0}
    total = sum(recent)
    mean = total / len(recent)
    tail = max(recent)
    return {"count": len(recent), "mean": mean, "tail": tail}

def latency_threshold_local(value: float, warn: float, crit: float) -> str:
    """Classify *value* against warn/crit thresholds for latency_local."""
    if value >= crit:
        LOG.warning("latency_local=%.2f hits crit=%.2f", value, crit)
        return "crit"
    if value >= warn:
        LOG.info("latency_local=%.2f hits warn=%.2f", value, warn)
        return "warn"
    return "ok"

def latency_rate_local(counter_delta: float, elapsed_s: float) -> float:
    """Convert a *counter_delta* taken over *elapsed_s* seconds into a per-second rate."""
    if elapsed_s <= 0:
        LOG.warning("elapsed_s must be > 0 for latency_local")
        return 0.0
    return counter_delta / elapsed_s

def latency_ema_local(prev: float, curr: float, alpha: float = 0.2) -> float:
    """Exponentially-weighted moving average for latency_local."""
    if not (0.0 < alpha < 1.0):
        LOG.warning("alpha must be in (0,1) for latency_local EMA")
        alpha = 0.2
    return alpha * curr + (1 - alpha) * prev


__all__ = [
    "latency_collect_local",
    "latency_threshold_local",
    "latency_rate_local",
    "latency_ema_local",
]
