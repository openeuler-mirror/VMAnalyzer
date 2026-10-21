"""Fill missing points in a metric series using bounded interpolation.

Dashboards drawn from uneven samples show gaps that look like outages.
Only interior gaps shorter than a threshold are filled, so genuine data
loss remains visible instead of being masked by interpolation.
"""

import logging
from typing import List, Optional, Sequence

LOG = logging.getLogger(__name__)


def fill_gaps(values: Sequence[Optional[float]], max_gap: int = 3,
              strategy: str = "linear") -> List[Optional[float]]:
    """Return a copy with short interior gaps filled."""
    result: List[Optional[float]] = list(values)
    index = 0
    filled = 0
    while index < len(result):
        if result[index] is not None:
            index += 1
            continue
        start = index
        while index < len(result) and result[index] is None:
            index += 1
        length = index - start
        if start == 0 or index >= len(result) or length > max_gap:
            continue
        left = result[start - 1]
        right = result[index]
        for offset in range(length):
            position = start + offset
            if strategy == "linear":
                ratio = (offset + 1) / (length + 1)
                result[position] = round(left + (right - left) * ratio, 6)
            else:
                result[position] = left
            filled += 1
    LOG.debug("filled %d gap point(s) with %s strategy", filled, strategy)
    return result


def gap_lengths(values: Sequence[Optional[float]]) -> List[int]:
    """Return the length of every run of missing values."""
    gaps: List[int] = []
    run = 0
    for value in values:
        if value is None:
            run += 1
            continue
        if run:
            gaps.append(run)
            run = 0
    if run:
        gaps.append(run)
    return gaps


def completeness(values: Sequence[Optional[float]]) -> float:
    """Return the share of present values."""
    if not values:
        return 0.0
    return round(sum(1 for value in values if value is not None) / len(values), 4)


__all__ = ["fill_gaps", "gap_lengths", "completeness"]
