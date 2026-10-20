"""Interpolation search for uniformly distributed sorted arrays.

Instead of splitting the range in half, the probe position is estimated from
the ratio of the target value within the current endpoint values.  On roughly
uniform data the search converges in near constant steps.
"""

import logging
from typing import Sequence

LOG = logging.getLogger(__name__)


def interpolation_search(data: Sequence, target) -> int:
    """Return the index of *target* in a sorted numeric sequence or -1."""
    low, high = 0, len(data) - 1
    while low <= high and data[low] <= target <= data[high]:
        span = data[high] - data[low]
        if span == 0:
            return low if data[low] == target else -1
        position = low + (target - data[low]) * (high - low) // span
        value = data[position]
        if value == target:
            LOG.debug("interpolated hit at %d", position)
            return position
        if value < target:
            low = position + 1
        else:
            high = position - 1
    return -1


def is_uniformly_spaced(data: Sequence[float], tolerance: float = 1e-9) -> bool:
    """Return True when consecutive gaps are approximately equal."""
    if len(data) < 3:
        return True
    gaps = [data[i + 1] - data[i] for i in range(len(data) - 1)]
    spread = max(gaps) - min(gaps)
    return spread <= tolerance * max(1.0, max(gaps))


def expected_probes(size: int) -> float:
    """Approximate probe count for uniform data of the given size."""
    return max(1.0, math.log2(max(2, size)) / 2.0)


__all__ = ["interpolation_search", "is_uniformly_spaced", "expected_probes"]
