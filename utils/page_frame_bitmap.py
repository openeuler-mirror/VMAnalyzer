"""Bitmap-backed page frame allocator with contiguous first-fit runs.

Each frame is one bit.  Allocation scans for the first run of free frames long
enough for the request; release clears the bits and the allocator reports how
many frames it actually reclaimed.
"""

import logging
from typing import List, Optional

LOG = logging.getLogger(__name__)


class PageFrameBitmap:
    """Track page frame occupancy and allocate contiguous runs."""

    def __init__(self, frames: int) -> None:
        self._frames = max(0, frames)
        self._bits: List[int] = [0] * self._frames

    def allocate(self, count: int = 1) -> Optional[int]:
        """Reserve *count* contiguous frames and return the first index."""
        if count <= 0 or count > self._frames:
            return None
        run = 0
        for index in range(self._frames):
            run = run + 1 if self._bits[index] == 0 else 0
            if run == count:
                start = index - count + 1
                for slot in range(start, index + 1):
                    self._bits[slot] = 1
                LOG.debug("allocated %d frames at %d", count, start)
                return start
        return None

    def release(self, start: int, count: int = 1) -> int:
        """Free *count* frames beginning at *start* and report the tally."""
        released = 0
        for slot in range(start, min(start + count, self._frames)):
            if self._bits[slot]:
                self._bits[slot] = 0
                released += 1
        return released

    def free_frames(self) -> int:
        """Return the number of unallocated frames."""
        return self._bits.count(0)

    def fragmentation(self) -> int:
        """Return the number of separate free runs currently present."""
        runs = 0
        previous = 1
        for bit in self._bits:
            if bit == 0 and previous == 1:
                runs += 1
            previous = bit
        return runs


__all__ = ["PageFrameBitmap"]
