"""Compute a symmetric trimmed mean for noisy metric series.

A single stalled IO or a burst of steal time can drag a plain mean far
above the steady state.  Trimming a fixed fraction from both tails gives a
robust central value without requiring a full histogram.
"""

import logging
from typing import Iterable, List

LOG = logging.getLogger(__name__)


def trimmed_mean(values: Iterable[float], fraction: float = 0.1) -> float:
    """Return the mean after dropping *fraction* from each tail."""
    sample = sorted(float(value) for value in values)
    if not sample:
        return 0.0
    if not 0.0 <= fraction < 0.5:
        raise ValueError("fraction must satisfy 0 <= fraction < 0.5")
    cut = int(len(sample) * fraction)
    kept: List[float] = sample[cut: len(sample) - cut] if cut else sample
    result = sum(kept) / len(kept)
    LOG.debug("trimmed mean %.4f from %d of %d samples", result, len(kept), len(sample))
    return result


def winsorized_mean(values: Iterable[float], fraction: float = 0.1) -> float:
    """Clamp both tails instead of dropping them, then average."""
    sample = sorted(float(value) for value in values)
    if not sample:
        return 0.0
    cut = int(len(sample) * fraction)
    if cut:
        low, high = sample[cut], sample[-cut - 1]
        sample = [min(max(value, low), high) for value in sample]
    return sum(sample) / len(sample)


__all__ = ["trimmed_mean", "winsorized_mean"]
