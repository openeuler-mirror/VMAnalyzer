"""Choose retry delays that spread clients instead of synchronising them.

Fixed exponential backoff makes every agent retry at the same instant after
a shared outage.  Full jitter or decorrelated jitter spreads the load and
dramatically reduces the thundering herd on recovery.
"""

import logging
import random
from typing import List

LOG = logging.getLogger(__name__)


def full_jitter(attempt: int, base: float = 0.5, cap: float = 30.0,
                rng: random.Random = None) -> float:
    """Return a uniform delay between zero and the capped exponential."""
    if attempt < 0:
        raise ValueError("attempt must not be negative")
    source = rng or random
    ceiling = min(cap, base * (2 ** attempt))
    return source.uniform(0.0, ceiling)


def decorrelated_jitter(previous: float, base: float = 0.5, cap: float = 30.0,
                        rng: random.Random = None) -> float:
    """Return a delay between *base* and three times the previous delay."""
    source = rng or random
    upper = min(cap, max(base, previous * 3.0))
    return source.uniform(base, upper)


def backoff_sequence(attempts: int, base: float = 0.5, cap: float = 30.0,
                     rng: random.Random = None) -> List[float]:
    """Build a jittered backoff sequence for planning a retry schedule."""
    delays = []
    for attempt in range(max(0, attempts)):
        delays.append(round(full_jitter(attempt, base, cap, rng), 3))
    LOG.debug("generated %d jittered retry delay(s)", len(delays))
    return delays


__all__ = ["full_jitter", "decorrelated_jitter", "backoff_sequence"]
