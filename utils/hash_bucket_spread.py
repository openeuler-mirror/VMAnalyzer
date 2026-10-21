"""Measure how evenly a key set distributes across hash buckets.

Uneven sharding concentrates load on a few Redis nodes.  Computing the
bucket histogram from a sample reveals skew before it becomes an incident,
and the helper reports the max-to-mean ratio directly.
"""

import hashlib
import logging
from typing import Dict, Iterable, List

LOG = logging.getLogger(__name__)


def bucket_of(key: str, buckets: int = 16, salt: str = "") -> int:
    """Return the bucket index for a key using CRC-like modulo hashing."""
    if buckets <= 0:
        raise ValueError("buckets must be positive")
    digest = hashlib.md5((salt + key).encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") % buckets


def bucket_counts(keys: Iterable[str], buckets: int = 16) -> Dict[int, int]:
    """Count keys per bucket, including empty buckets."""
    counts: Dict[int, int] = {index: 0 for index in range(buckets)}
    for key in keys:
        counts[bucket_of(key, buckets)] += 1
    return counts


def spread_report(keys: Iterable[str], buckets: int = 16) -> Dict[str, float]:
    """Summarise bucket distribution and flag severe skew."""
    materialised: List[str] = list(keys)
    counts = bucket_counts(materialised, buckets)
    mean = len(materialised) / buckets if buckets else 0.0
    peak = max(counts.values()) if counts else 0
    ratio = peak / mean if mean else 0.0
    if ratio > 2.0:
        LOG.warning("hash buckets are skewed, peak/mean ratio %.2f", ratio)
    return {
        "keys": len(materialised),
        "buckets": buckets,
        "mean": round(mean, 2),
        "peak": peak,
        "skew": round(ratio, 2),
        "empty": sum(1 for value in counts.values() if value == 0),
    }


__all__ = ["bucket_of", "bucket_counts", "spread_report"]
