"""Estimate clock drift between a local clock and sampled remote clocks.

Guest clocks skew slowly and silently.  Comparing a monotonic local
reference with remote timestamps captured at known local instants yields a
drift estimate that is good enough to flag guests needing NTP repair.
"""

import logging
import time
from typing import Iterable, Optional

LOG = logging.getLogger(__name__)


def drift_seconds(remote_timestamp: float, local_reference: Optional[float] = None) -> float:
    """Return how far the remote clock is ahead of the local reference."""
    reference = time.time() if local_reference is None else local_reference
    drift = float(remote_timestamp) - reference
    LOG.debug("clock drift measured at %.3f seconds", drift)
    return drift


def median_drift(samples: Iterable[float]) -> float:
    """Return the median drift across several paired samples."""
    values = sorted(float(sample) for sample in samples)
    if not values:
        return 0.0
    middle = len(values) // 2
    if len(values) % 2:
        return values[middle]
    return round((values[middle - 1] + values[middle]) / 2.0, 6)


def drift_status(drift: float, warn: float = 1.0, critical: float = 5.0) -> str:
    """Classify an absolute drift value into an operational status."""
    magnitude = abs(drift)
    if magnitude >= critical:
        return "critical"
    if magnitude >= warn:
        return "warning"
    return "ok"


__all__ = ["drift_seconds", "median_drift", "drift_status"]
