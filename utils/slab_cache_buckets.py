"""Slab cache bucket sizing and occupancy accounting.

Object sizes are rounded up to the next power of two so a small number of
uniform slabs serve many allocation sizes.  The module groups requests into
buckets and reports the internal waste introduced by that rounding.
"""

import logging
from typing import Dict, List, Sequence

LOG = logging.getLogger(__name__)


def bucket_for_size(size: int) -> int:
    """Return the power-of-two bucket that can hold *size* bytes."""
    if size <= 0:
        return 0
    return 1 << (size - 1).bit_length()


def build_slab_map(sizes: Sequence[int]) -> Dict[int, List[int]]:
    """Group object sizes into slabs keyed by their bucket size."""
    mapping: Dict[int, List[int]] = {}
    for size in sizes:
        mapping.setdefault(bucket_for_size(size), []).append(size)
    LOG.debug("sizes spread across %d buckets", len(mapping))
    return mapping


def waste_ratio(sizes: Sequence[int]) -> float:
    """Return the fraction of allocated bytes wasted by rounding up."""
    if not sizes:
        return 0.0
    used = sum(sizes)
    allocated = sum(bucket_for_size(size) for size in sizes)
    if allocated == 0:
        return 0.0
    ratio = (allocated - used) / allocated
    LOG.debug("slab waste ratio %.4f", ratio)
    return ratio


def busiest_bucket(sizes: Sequence[int]) -> int:
    """Return the bucket size holding the most objects."""
    mapping = build_slab_map(sizes)
    if not mapping:
        return 0
    return max(mapping, key=lambda bucket: len(mapping[bucket]))


__all__ = ["bucket_for_size", "build_slab_map", "waste_ratio", "busiest_bucket"]
