"""Jump search over sorted sequences using a fixed stride.

The sequence is scanned in blocks of roughly the square root of its length
until a block that could contain the target is found, then a linear scan
inside that block locates the element.  It is a good fit for arrays where
backward jumps are cheap but random access is not.
"""

import logging
import math
from typing import Optional, Sequence

LOG = logging.getLogger(__name__)


def optimal_block_size(size: int) -> int:
    """Return the block size that minimises jump search comparisons."""
    return max(1, math.isqrt(size))


def jump_search(data: Sequence, target, block: Optional[int] = None) -> int:
    """Return the index of *target* in a sorted sequence or -1."""
    size = len(data)
    if size == 0:
        return -1
    step = block if block else optimal_block_size(size)
    previous = 0
    current = step
    while current < size and data[current] < target:
        previous = current
        current += step
    for index in range(previous, min(current, size)):
        if data[index] == target:
            LOG.debug("jump search hit at %d", index)
            return index
        if data[index] > target:
            break
    return -1


def jump_count(size: int, block: Optional[int] = None) -> int:
    """Number of blocks a full scan would visit for the given size."""
    step = block if block else optimal_block_size(size)
    return (size + step - 1) // step


__all__ = ["optimal_block_size", "jump_search", "jump_count"]
