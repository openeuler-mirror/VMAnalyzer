"""Group timestamps into coarse age buckets for retention dashboards.

Retention policies are easier to reason about in qualitative buckets
(hour, day, week, month) than in raw seconds.  The helper maps a timestamp
to a stable bucket label without pulling in dateutil.
"""

import logging
import time
from typing import Dict, List

LOG = logging.getLogger(__name__)

BUCKET_BOUNDS = (
    ("fresh", 3600.0),
    ("hour", 86400.0),
    ("day", 7 * 86400.0),
    ("week", 30 * 86400.0),
    ("month", 365 * 86400.0),
)


def age_of(timestamp: float, now: float = None) -> float:
    """Return the non-negative age of *timestamp* in seconds."""
    reference = time.time() if now is None else now
    return max(0.0, reference - float(timestamp))


def bucket_name(timestamp: float, now: float = None) -> str:
    """Return the qualitative bucket for a timestamp."""
    age = age_of(timestamp, now)
    for name, limit in BUCKET_BOUNDS:
        if age < limit:
            return name
    return "stale"


def bucket_counts(timestamps: List[float], now: float = None) -> Dict[str, int]:
    """Count how many timestamps fall into each bucket label."""
    counts: Dict[str, int] = {}
    for timestamp in timestamps:
        name = bucket_name(timestamp, now)
        counts[name] = counts.get(name, 0) + 1
    LOG.debug("bucket counts %s", counts)
    return counts


__all__ = ["BUCKET_BOUNDS", "age_of", "bucket_name", "bucket_counts"]
