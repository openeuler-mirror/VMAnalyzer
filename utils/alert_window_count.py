"""Count alert firings inside a set of aligned evaluation windows.

Alert policies are defined over windows such as "three times in ten
minutes".  Counting per window makes the policy evaluation explicit and
avoids off-by-one errors from timestamp subtraction.
"""

import logging
from typing import Dict, Iterable, List

LOG = logging.getLogger(__name__)


def window_index(timestamp: float, window: float, origin: float = 0.0) -> int:
    """Return the aligned window index containing *timestamp*."""
    if window <= 0:
        raise ValueError("window must be positive")
    return int((float(timestamp) - origin) // window)


def count_by_window(timestamps: Iterable[float], window: float,
                    origin: float = 0.0) -> Dict[int, int]:
    """Count timestamps per aligned window index."""
    counts: Dict[int, int] = {}
    for timestamp in timestamps:
        index = window_index(timestamp, window, origin)
        counts[index] = counts.get(index, 0) + 1
    LOG.debug("counted alerts in %d window(s)", len(counts))
    return counts


def windows_over(timestamps: Iterable[float], window: float, threshold: int,
                 origin: float = 0.0) -> List[int]:
    """Return window indices whose count exceeds *threshold*."""
    counts = count_by_window(timestamps, window, origin)
    return sorted(index for index, count in counts.items() if count > threshold)


__all__ = ["window_index", "count_by_window", "windows_over"]
