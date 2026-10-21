"""Align timestamps to fixed reporting slots with configurable offset.

Collectors occasionally emit samples a few seconds late, which creates
near-duplicate buckets at slot boundaries.  Aligning down to the slot start
guarantees one bucket per slot regardless of arrival jitter.
"""

import logging
from typing import List

LOG = logging.getLogger(__name__)


def align_down(timestamp: float, slot_seconds: int, offset: int = 0) -> float:
    """Round *timestamp* down to the start of its slot."""
    if slot_seconds <= 0:
        raise ValueError("slot_seconds must be positive")
    shifted = timestamp - offset
    aligned = shifted - (shifted % slot_seconds)
    return float(aligned + offset)


def align_up(timestamp: float, slot_seconds: int, offset: int = 0) -> float:
    """Round *timestamp* up to the next slot boundary."""
    if slot_seconds <= 0:
        raise ValueError("slot_seconds must be positive")
    down = align_down(timestamp, slot_seconds, offset)
    return float(down if down == timestamp else down + slot_seconds)


def distinct_slots(timestamps: List[float], slot_seconds: int) -> List[float]:
    """Return sorted unique slot starts for a batch of timestamps."""
    slots = sorted({align_down(value, slot_seconds) for value in timestamps})
    LOG.debug("mapped %d timestamps to %d slot(s)", len(timestamps), len(slots))
    return slots


__all__ = ["align_down", "align_up", "distinct_slots"]
