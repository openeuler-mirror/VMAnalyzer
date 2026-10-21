"""Convert byte rates into decimal and binary megabit notation.

Network limits are quoted in Mbps while kernel counters report bytes per
second.  Converting consistently avoids an eightfold error in capacity
calculations.
"""

import logging
from typing import Dict

LOG = logging.getLogger(__name__)

BITS_PER_BYTE = 8


def bytes_to_megabits(bytes_per_second: float, binary: bool = False) -> float:
    """Return the rate in megabits using decimal or binary units."""
    base = 1024.0 if binary else 1000.0
    return round(bytes_per_second * BITS_PER_BYTE / (base * base), 3)


def megabits_to_bytes(megabits: float, binary: bool = False) -> float:
    """Return bytes per second for a megabit rate."""
    base = 1024.0 if binary else 1000.0
    return megabits * base * base / BITS_PER_BYTE


def describe(bytes_per_second: float) -> Dict[str, float]:
    """Return both unit conventions for the same rate."""
    result = {
        "mbps": bytes_to_megabits(bytes_per_second),
        "mibps": bytes_to_megabits(bytes_per_second, binary=True),
        "bytes_per_second": float(bytes_per_second),
    }
    LOG.debug("bandwidth description %s", result)
    return result


__all__ = ["BITS_PER_BYTE", "bytes_to_megabits", "megabits_to_bytes", "describe"]
