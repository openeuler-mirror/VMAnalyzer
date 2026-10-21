"""Convert linear ratios into decibels and back.

Signal-to-noise and degradation metrics are easier to compare in decibels.
Zero and negative ratios are rejected explicitly rather than producing
infinite values.
"""

import logging
import math
from typing import Iterable, List

LOG = logging.getLogger(__name__)


def to_db(ratio: float, power: bool = False) -> float:
    """Return the decibel value of a positive ratio."""
    value = float(ratio)
    if value <= 0:
        raise ValueError("ratio must be positive to convert into decibels")
    factor = 10.0 if power else 20.0
    return round(factor * math.log10(value), 4)


def from_db(decibels: float, power: bool = False) -> float:
    """Return the linear ratio for a decibel value."""
    factor = 10.0 if power else 20.0
    return round(10 ** (float(decibels) / factor), 6)


def noise_floor(values: Iterable[float]) -> float:
    """Return the minimum positive ratio converted to decibels."""
    positives = [float(value) for value in values if float(value) > 0]
    if not positives:
        LOG.warning("no positive values available for a noise floor")
        return 0.0
    return to_db(min(positives))


def spread_db(values: Iterable[float]) -> List[float]:
    """Convert a series of ratios into decibels, skipping invalid values."""
    result = []
    for value in values:
        if float(value) <= 0:
            continue
        result.append(to_db(value))
    return result


__all__ = ["to_db", "from_db", "noise_floor", "spread_db"]
