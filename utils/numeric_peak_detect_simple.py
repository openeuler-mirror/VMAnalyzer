"""Detect local maxima using a configurable neighbour window.

Prominent spikes matter more than the exact shape of a metric curve.  A
plain local-maximum scan with a minimum separation avoids reporting every
sample of a plateau as a separate peak.
"""

import logging
from typing import Iterable, List

LOG = logging.getLogger(__name__)


def detect_peaks(values: Iterable[float], window: int = 2,
                 min_prominence: float = 0.0) -> List[int]:
    """Return indices that are the maximum of their local neighbourhood."""
    sample = [float(value) for value in values]
    if window < 1:
        raise ValueError("window must be at least 1")
    peaks: List[int] = []
    for index, value in enumerate(sample):
        low = max(0, index - window)
        high = min(len(sample), index + window + 1)
        neighbours = sample[low:high]
        if value < max(neighbours):
            continue
        if value - min(neighbours) < min_prominence:
            continue
        if peaks and index - peaks[-1] <= window:
            if value > sample[peaks[-1]]:
                peaks[-1] = index
            continue
        peaks.append(index)
    LOG.debug("detected %d peak(s) in %d samples", len(peaks), len(sample))
    return peaks


def peak_values(values: Iterable[float], window: int = 2) -> List[float]:
    """Return the values at all detected peak indices."""
    sample = [float(value) for value in values]
    return [sample[index] for index in detect_peaks(sample, window=window)]


__all__ = ["detect_peaks", "peak_values"]
