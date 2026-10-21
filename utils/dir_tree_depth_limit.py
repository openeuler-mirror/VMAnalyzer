"""Enforce a maximum directory depth on reported file inventories.

Deep directory trees slow down recursive scans and often come from stray
build caches.  Flagging deep entries lets an operator prune them before a
collection cycle walks millions of inodes.
"""

import logging
from typing import Dict, Iterable, List

LOG = logging.getLogger(__name__)


def depth_of(path: str) -> int:
    """Return the number of directory separators in a normalised path."""
    cleaned = path.strip("/").replace("\\", "/")
    if not cleaned:
        return 0
    return cleaned.count("/") + 1


def deep_entries(paths: Iterable[str], limit: int = 8) -> List[str]:
    """Return paths whose depth exceeds *limit*."""
    if limit < 0:
        raise ValueError("limit must not be negative")
    flagged = [path for path in paths if depth_of(path) > limit]
    if flagged:
        LOG.warning("%d path(s) exceed the depth limit of %d", len(flagged), limit)
    return flagged


def depth_histogram(paths: Iterable[str]) -> Dict[int, int]:
    """Count paths per depth level."""
    histogram: Dict[int, int] = {}
    for path in paths:
        depth = depth_of(path)
        histogram[depth] = histogram.get(depth, 0) + 1
    return dict(sorted(histogram.items()))


__all__ = ["depth_of", "deep_entries", "depth_histogram"]
