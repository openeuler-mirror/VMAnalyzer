"""Detect paths that collide on case-insensitive filesystems.

A collection tree built on Linux can become unusable when copied to a
Windows or macOS share because ``VM1.log`` and ``vm1.log`` occupy the same
directory entry.  Checking before export avoids silent data loss.
"""

import logging
from typing import Dict, List

LOG = logging.getLogger(__name__)


def case_key(path: str) -> str:
    """Return the fold key used for case-insensitive comparison."""
    return path.replace("\\", "/").rstrip("/").lower()


def case_conflicts(paths: List[str]) -> Dict[str, List[str]]:
    """Group paths that differ only by case."""
    groups: Dict[str, List[str]] = {}
    for path in paths:
        groups.setdefault(case_key(path), []).append(path)
    conflicts = {key: items for key, items in groups.items() if len(set(items)) > 1}
    if conflicts:
        LOG.warning("detected %d case-only conflict(s)", len(conflicts))
    return conflicts


def is_portable(paths: List[str]) -> bool:
    """Return True when the tree can be copied to a case-insensitive host."""
    return not case_conflicts(paths)


__all__ = ["case_key", "case_conflicts", "is_portable"]
