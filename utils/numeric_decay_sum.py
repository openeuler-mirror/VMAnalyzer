"""Accumulate a time-decayed sum of samples (exponential forgetting).

Long-running agents cannot keep every sample in memory.  A decayed sum
captures recent history with a single float and is a cheap alternative to
a sliding window when only the trend magnitude matters.
"""

import logging
import time
from typing import Iterable, Optional

LOG = logging.getLogger(__name__)


def decayed_sum(samples: Iterable[float], decay: float = 0.9,
                now: Optional[float] = None) -> float:
    """Fold samples so each older value contributes *decay* times less."""
    if not 0.0 < decay <= 1.0:
        raise ValueError("decay must satisfy 0 < decay <= 1")
    total = 0.0
    count = 0
    for sample in samples:
        total = total * decay + float(sample)
        count += 1
    LOG.debug("decayed sum over %d samples with factor %.2f", count, decay)
    return total


def decayed_average(samples: Iterable[float], decay: float = 0.9) -> float:
    """Normalise the decayed sum by the decayed weight total."""
    total = weight = 0.0
    for sample in samples:
        total = total * decay + float(sample)
        weight = weight * decay + 1.0
    return total / weight if weight else 0.0


def age_weight(age_seconds: float, half_life: float = 300.0,
               now: Optional[float] = None) -> float:
    """Return the exponential weight of a sample of the given age."""
    if half_life <= 0:
        raise ValueError("half_life must be positive")
    reference = time.time() if now is None else now
    age = max(0.0, reference - age_seconds)
    return 0.5 ** (age / half_life)


__all__ = ["decayed_sum", "decayed_average", "age_weight"]
