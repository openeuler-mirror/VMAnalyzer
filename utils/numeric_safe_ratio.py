"""Divide two counters without raising on zero or non-numeric input.

Capacity and saturation metrics are frequently derived from counters that
may legitimately be zero during startup.  Returning ``None`` for an
undefined ratio lets callers distinguish "no traffic" from a real value.
"""

import logging
from typing import Optional, Union

LOG = logging.getLogger(__name__)

Number = Union[int, float]


def safe_ratio(numerator: Optional[Number], denominator: Optional[Number],
               scale: float = 1.0) -> Optional[float]:
    """Return ``numerator / denominator * scale`` or None when undefined."""
    if numerator is None or denominator is None:
        return None
    try:
        divisor = float(denominator)
        if divisor == 0.0:
            LOG.debug("ratio skipped because the denominator is zero")
            return None
        return float(numerator) / divisor * float(scale)
    except (TypeError, ValueError):
        LOG.warning("non-numeric ratio inputs %r / %r", numerator, denominator)
        return None


def percent(part: Optional[Number], whole: Optional[Number],
            digits: int = 2) -> Optional[float]:
    """Return the percentage of *part* in *whole*, rounded to *digits*."""
    ratio = safe_ratio(part, whole, scale=100.0)
    return None if ratio is None else round(ratio, digits)


def clamp_ratio(value: Optional[float], low: float = 0.0, high: float = 1.0) -> float:
    """Clamp a ratio into ``[low, high]``, treating None as *low*."""
    if value is None:
        return low
    return max(low, min(high, value))


__all__ = ["Number", "safe_ratio", "percent", "clamp_ratio"]
