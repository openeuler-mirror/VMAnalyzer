"""Coalescing of adjacent free blocks in a memory free list.

Free regions are given as ``(start, size)`` pairs.  After sorting by start,
touching or overlapping regions are merged so the free list always describes
maximal contiguous extents, which is what allocation routines want.
"""

import logging
from typing import Iterable, List, Tuple

LOG = logging.getLogger(__name__)

Block = Tuple[int, int]


def coalesce(blocks: Iterable[Block]) -> List[Block]:
    """Merge free blocks whose ranges touch or overlap."""
    ordered = sorted(blocks)
    merged: List[Block] = []
    for start, size in ordered:
        end = start + size
        if merged and start <= merged[-1][0] + merged[-1][1]:
            previous_start, previous_size = merged[-1]
            merged[-1] = (previous_start, max(previous_start + previous_size, end) - previous_start)
        else:
            merged.append((start, size))
    LOG.debug("coalesced %d blocks into %d", len(ordered), len(merged))
    return merged


def largest_free_block(blocks: Iterable[Block]) -> int:
    """Return the size of the largest coalesced free region."""
    return max((size for _, size in coalesce(blocks)), default=0)


def total_free(blocks: Iterable[Block]) -> int:
    """Return the total free bytes after coalescing."""
    return sum(size for _, size in coalesce(blocks))


def fragmentation_count(blocks: Iterable[Block]) -> int:
    """Return how many distinct free regions remain after coalescing."""
    return len(coalesce(blocks))


__all__ = ["coalesce", "largest_free_block", "total_free", "fragmentation_count"]
