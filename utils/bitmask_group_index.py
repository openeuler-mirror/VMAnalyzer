"""Index small integer sets as bitmasks for fast membership checks.

Feature flags and CPU flag sets fit comfortably in Python integers, and a
bitmask test is much cheaper than a set lookup inside hot collection loops.
The helpers keep the conversion logic in one tested place.
"""

import logging
from typing import Dict, Iterable, List

LOG = logging.getLogger(__name__)


def to_mask(values: Iterable[int]) -> int:
    """Pack non-negative integers into a bitmask."""
    mask = 0
    for value in values:
        number = int(value)
        if number < 0:
            raise ValueError("bit positions must be non-negative")
        mask |= 1 << number
    return mask


def from_mask(mask: int, width: int = 0) -> List[int]:
    """Expand a bitmask into ascending bit positions."""
    positions: List[int] = []
    index = 0
    limit = max(width, mask.bit_length())
    while index < limit:
        if mask & (1 << index):
            positions.append(index)
        index += 1
    LOG.debug("expanded mask into %d position(s)", len(positions))
    return positions


def group_masks(flags: Dict[str, Iterable[int]]) -> Dict[str, int]:
    """Convert every flag set in *flags* to a bitmask."""
    return {name: to_mask(values) for name, values in flags.items()}


def shared_positions(masks: Iterable[int]) -> List[int]:
    """Return bit positions set in every supplied mask."""
    items = list(masks)
    if not items:
        return []
    combined = items[0]
    for mask in items[1:]:
        combined &= mask
    return from_mask(combined)


__all__ = ["to_mask", "from_mask", "group_masks", "shared_positions"]
