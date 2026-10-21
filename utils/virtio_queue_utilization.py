"""Estimate virtio queue utilisation from request counters.

A saturated virtio queue manifests as rising latency long before packet
drops appear.  Comparing processed requests to queue depth over an interval
gives a utilisation estimate suitable for early warning.
"""

import logging
from typing import Dict

LOG = logging.getLogger(__name__)


def utilisation(requests: int, queue_size: int, intervals: int) -> float:
    """Return queue utilisation as a fraction of capacity."""
    if queue_size <= 0 or intervals <= 0:
        return 0.0
    capacity = queue_size * intervals
    return round(min(1.0, requests / capacity), 4)


def state(value: float) -> str:
    """Classify utilisation into a coarse operational state."""
    if value >= 0.9:
        return "saturated"
    if value >= 0.7:
        return "busy"
    return "idle"


def summary(requests: int, queue_size: int, intervals: int) -> Dict[str, object]:
    """Return utilisation plus its state and headroom."""
    value = utilisation(requests, queue_size, intervals)
    result = {"utilisation": value, "state": state(value),
              "headroom": round(max(0.0, 1.0 - value), 4)}
    if value >= 0.9:
        LOG.warning("virtio queue appears saturated at %.1f%%", value * 100)
    return result


__all__ = ["utilisation", "state", "summary"]
