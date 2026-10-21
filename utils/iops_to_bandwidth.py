"""Estimate bandwidth implied by an IOPS figure and average block size.

Storage teams quote IOPS while network teams quote megabytes per second.
Converting between them with an explicit block size keeps capacity
discussions concrete and reproducible.
"""

import logging
from typing import Dict

LOG = logging.getLogger(__name__)


def iops_to_mb(iops: float, block_kb: float = 4.0) -> float:
    """Return the sequential bandwidth in megabytes per second."""
    if block_kb <= 0:
        raise ValueError("block_kb must be positive")
    return round(float(iops) * block_kb / 1024.0, 3)


def mb_to_iops(megabytes_per_second: float, block_kb: float = 4.0) -> float:
    """Return the IOPS needed to sustain the bandwidth."""
    if block_kb <= 0:
        raise ValueError("block_kb must be positive")
    return round(float(megabytes_per_second) * 1024.0 / block_kb, 2)


def translate(iops: float, block_kb: float = 4.0) -> Dict[str, float]:
    """Return bandwidth for several common block sizes."""
    result = {str(size): iops_to_mb(iops, size) for size in (4.0, 8.0, 64.0, block_kb)}
    LOG.debug("translated %.1f IOPS into bandwidth estimates", iops)
    return result


__all__ = ["iops_to_mb", "mb_to_iops", "translate"]
