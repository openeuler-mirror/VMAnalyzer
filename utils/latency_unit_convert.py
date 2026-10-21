"""Convert latency values between seconds, milliseconds and microseconds.

Collectors report latency in the unit their tool happens to use, which makes
threshold comparison error prone.  A single conversion entry point keeps
thresholds expressed consistently in milliseconds.
"""

import logging
from typing import Dict

LOG = logging.getLogger(__name__)

FACTORS = {"s": 1000.0, "ms": 1.0, "us": 0.001, "ns": 0.000001}


def to_milliseconds(value: float, unit: str) -> float:
    """Convert *value* from *unit* into milliseconds."""
    key = unit.strip().lower()
    if key not in FACTORS:
        raise ValueError("unsupported latency unit {!r}".format(unit))
    return round(float(value) * FACTORS[key], 6)


def from_milliseconds(value: float, unit: str) -> float:
    """Convert milliseconds into the requested unit."""
    key = unit.strip().lower()
    if key not in FACTORS:
        raise ValueError("unsupported latency unit {!r}".format(unit))
    return round(float(value) / FACTORS[key], 6)


def describe(value: float, unit: str) -> Dict[str, float]:
    """Return the latency expressed in every supported unit."""
    milliseconds = to_milliseconds(value, unit)
    result = {name: from_milliseconds(milliseconds, name) for name in FACTORS}
    LOG.debug("latency description %s", result)
    return result


__all__ = ["FACTORS", "to_milliseconds", "from_milliseconds", "describe"]
