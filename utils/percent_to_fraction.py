"""Convert between percentage and fraction representations safely.

Threshold configuration appears in both forms, and mixing them causes
off-by-100 errors that are hard to spot in reviews.  Explicit helpers make
the intended form obvious at every call site.
"""

import logging
from typing import Iterable, List, Optional

LOG = logging.getLogger(__name__)


def to_fraction(percent: float, clamp: bool = True) -> float:
    """Convert a percentage into a 0..1 fraction."""
    value = float(percent) / 100.0
    if clamp and not 0.0 <= value <= 1.0:
        LOG.warning("percentage %.2f is outside 0..100 and was clamped", percent)
        return max(0.0, min(1.0, value))
    return value


def to_percent(fraction: float, digits: int = 2) -> float:
    """Convert a 0..1 fraction into a percentage."""
    return round(float(fraction) * 100.0, digits)


def detect_form(values: Iterable[float], threshold: float = 1.5) -> Optional[str]:
    """Guess whether a value series is expressed as fractions or percentages."""
    sample = [float(value) for value in values]
    if not sample:
        return None
    largest = max(abs(value) for value in sample)
    form = "fraction" if largest <= threshold else "percent"
    LOG.debug("detected %s representation from max %.2f", form, largest)
    return form


def convert(values: Iterable[float], target: str) -> List[float]:
    """Convert a series into the requested representation."""
    sample = list(values)
    form = detect_form(sample)
    if form == target or form is None:
        return [float(value) for value in sample]
    if target == "fraction":
        return [to_fraction(value) for value in sample]
    return [to_percent(value) for value in sample]


__all__ = ["to_fraction", "to_percent", "detect_form", "convert"]
