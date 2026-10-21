"""Compute evenly spaced histogram bin edges for a value series.

Equal-width bins keep dashboards comparable across hosts, but naively
dividing by a fixed width produces empty leading or trailing bins.  The
helper clamps to the observed range and guarantees at least one bin.
"""

import logging
from typing import Iterable, List

LOG = logging.getLogger(__name__)


def bin_edges(values: Iterable[float], bins: int = 10) -> List[float]:
    """Return ``bins + 1`` ascending edges spanning the observed values."""
    sample = [float(value) for value in values]
    if not sample:
        LOG.debug("no samples supplied, returning a single zero edge")
        return [0.0]
    count = max(1, int(bins))
    low, high = min(sample), max(sample)
    if abs(high - low) < 1e-12:
        high = low + 1.0
    step = (high - low) / count
    edges = [low + step * index for index in range(count + 1)]
    edges[-1] = high
    return edges


def assign_bin(value: float, edges: List[float]) -> int:
    """Return the index of the bin that owns *value* (last bin is closed)."""
    if len(edges) < 2:
        return 0
    for index in range(len(edges) - 1):
        if value < edges[index + 1]:
            return index
    return len(edges) - 2


def bin_widths(edges: List[float]) -> List[float]:
    """Return the width of each consecutive bin."""
    widths = [round(edges[i + 1] - edges[i], 9) for i in range(len(edges) - 1)]
    LOG.debug("computed %d bin widths", len(widths))
    return widths


__all__ = ["bin_edges", "assign_bin", "bin_widths"]
