"""Simplified buddy allocator over power-of-two blocks.

Free blocks are kept in per-order lists.  An allocation of order k splits a
larger free block repeatedly, while a release merges the freed block with its
buddy whenever that buddy is also free, cascading up the orders.
"""

import logging
import math
from typing import Dict, List, Optional

LOG = logging.getLogger(__name__)


class BuddyAllocator:
    """Manage free blocks per order and coalesce buddies on release."""

    def __init__(self, total_blocks: int) -> None:
        if total_blocks > 0:
            self._order = int(round(math.log2(total_blocks)))
        else:
            self._order = 0
        self._order = max(0, self._order)
        self._free: Dict[int, List[int]] = {self._order: [0]}

    def allocate(self, order: int) -> Optional[int]:
        """Allocate a block of *order*, splitting a larger buddy if needed."""
        for current in range(order, self._order + 1):
            pool = self._free.get(current)
            if not pool:
                continue
            block = pool.pop()
            while current > order:
                current -= 1
                buddy = block + (1 << current)
                self._free.setdefault(current, []).append(buddy)
            LOG.debug("allocated order %d at block %d", order, block)
            return block
        LOG.info("allocation of order %d failed", order)
        return None

    def release(self, block: int, order: int) -> int:
        """Return a block to the free lists, merging with its buddy."""
        current = order
        while current < self._order:
            buddy = block ^ (1 << current)
            pool = self._free.setdefault(current, [])
            if buddy not in pool:
                break
            pool.remove(buddy)
            block = min(block, buddy)
            current += 1
        self._free.setdefault(current, []).append(block)
        return current

    def free_blocks(self) -> int:
        """Return the total number of free blocks across all orders."""
        return sum(len(pool) for pool in self._free.values())


__all__ = ["BuddyAllocator"]
