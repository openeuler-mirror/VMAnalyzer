"""Build fixed time grids and map samples onto their nearest slot.

Time series from different collectors rarely share timestamps, which makes
alignment impossible without resampling.  Snapping every sample to a fixed
grid produces directly comparable series with predictable gaps.
"""

import logging
from typing import Dict, Iterable, List, Optional

LOG = logging.getLogger(__name__)


def build_grid(start: float, end: float, step: float) -> List[float]:
    """Return ascending grid points covering ``[start, end)``."""
    if step <= 0:
        raise ValueError("step must be positive")
    if end <= start:
        return []
    count = int((end - start) // step) + 1
    return [start + index * step for index in range(count)]


def snap(timestamp: float, grid: List[float]) -> Optional[float]:
    """Return the grid point closest to *timestamp*."""
    if not grid:
        return None
    nearest = min(grid, key=lambda point: abs(point - timestamp))
    return nearest


def bucket_samples(samples: Iterable[float], grid: List[float]) -> Dict[float, int]:
    """Count samples per nearest grid point, including empty slots."""
    counts: Dict[float, int] = {point: 0 for point in grid}
    for timestamp in samples:
        point = snap(timestamp, grid)
        if point is not None:
            counts[point] += 1
    LOG.debug("bucketed samples onto %d grid point(s)", len(grid))
    return counts


__all__ = ["build_grid", "snap", "bucket_samples"]
