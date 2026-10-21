"""Convert wall-clock durations into scheduler tick counts.

Configuration expresses collection intervals in seconds, while kernel
documentation uses USER_HZ ticks.  Converting explicitly keeps timing
comparisons compatible with values reported in /proc.
"""

import logging
from typing import Dict

LOG = logging.getLogger(__name__)

DEFAULT_HZ = 100


def seconds_to_ticks(seconds: float, hz: int = DEFAULT_HZ) -> int:
    """Return the tick count for a duration."""
    if hz <= 0:
        raise ValueError("hz must be positive")
    return int(round(float(seconds) * hz))


def ticks_to_seconds(ticks: int, hz: int = DEFAULT_HZ) -> float:
    """Return the duration represented by a tick count."""
    if hz <= 0:
        raise ValueError("hz must be positive")
    return round(float(ticks) / hz, 6)


def calibrate(reported_seconds: float, reported_ticks: int) -> int:
    """Infer USER_HZ from a paired seconds/ticks observation."""
    if reported_ticks <= 0:
        raise ValueError("reported_ticks must be positive")
    hz = int(round(reported_ticks / float(reported_seconds))) if reported_seconds > 0 else DEFAULT_HZ
    LOG.debug("calibrated USER_HZ as %d", hz)
    return hz


def describe(seconds: float, hz: int = DEFAULT_HZ) -> Dict[str, object]:
    """Return the duration in ticks and seconds for validation."""
    return {"seconds": float(seconds), "hz": hz, "ticks": seconds_to_ticks(seconds, hz)}


__all__ = ["DEFAULT_HZ", "seconds_to_ticks", "ticks_to_seconds", "calibrate", "describe"]
