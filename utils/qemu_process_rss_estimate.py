"""Estimate QEMU process memory overhead beyond guest RAM.

Host capacity planning must account for the qemu process footprint.  Using
guest RAM and observed RSS, the helper derives a per-guest overhead factor
that is far more realistic than a fixed constant.
"""

import logging
from typing import Dict

LOG = logging.getLogger(__name__)


def overhead_bytes(rss_bytes: int, guest_ram_bytes: int) -> int:
    """Return the part of RSS attributed to emulation overhead."""
    return max(0, int(rss_bytes) - int(guest_ram_bytes))


def overhead_ratio(rss_bytes: int, guest_ram_bytes: int) -> float:
    """Return overhead as a fraction of guest RAM."""
    if guest_ram_bytes <= 0:
        return 0.0
    return round(overhead_bytes(rss_bytes, guest_ram_bytes) / guest_ram_bytes, 4)


def summary(rss_bytes: int, guest_ram_bytes: int,
            warning: float = 0.2) -> Dict[str, object]:
    """Return overhead figures and a warning flag."""
    ratio = overhead_ratio(rss_bytes, guest_ram_bytes)
    result = {
        "overhead": overhead_bytes(rss_bytes, guest_ram_bytes),
        "ratio": ratio,
        "high": ratio > warning,
    }
    if result["high"]:
        LOG.info("qemu overhead ratio %.3f exceeds the %.3f warning level", ratio, warning)
    return result


__all__ = ["overhead_bytes", "overhead_ratio", "summary"]
