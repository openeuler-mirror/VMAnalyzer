"""Plan which rotated log files to keep given size and count limits.

Unbounded growth of collector logs is a common cause of full root
filesystems on hypervisors.  This planner selects survivors and reports the
bytes that can be reclaimed.
"""

import logging
from typing import Dict, List, Tuple

LOG = logging.getLogger(__name__)


def plan_rotation(files: List[Tuple[str, int]], keep: int = 7,
                  max_bytes: int = 200 * 1024 * 1024) -> Dict[str, object]:
    """Select files to keep by age order and total size budget."""
    if keep < 0:
        raise ValueError("keep must not be negative")
    ordered = sorted(files, key=lambda item: item[1], reverse=True)
    survivors: List[str] = []
    removed: List[str] = []
    total = 0
    for name, size in ordered:
        if len(survivors) < keep and total + size <= max_bytes:
            survivors.append(name)
            total += size
        else:
            removed.append(name)
    reclaimed = sum(size for name, size in ordered if name in removed)
    LOG.info("rotation plan keeps %d file(s) and reclaims %d bytes",
             len(survivors), reclaimed)
    return {
        "keep": survivors,
        "remove": removed,
        "kept_bytes": total,
        "reclaimed_bytes": reclaimed,
    }


def exceeds_budget(files: List[Tuple[str, int]], max_bytes: int) -> bool:
    """Return True when the combined size exceeds the budget."""
    return sum(size for _, size in files) > max_bytes


__all__ = ["plan_rotation", "exceeds_budget"]
