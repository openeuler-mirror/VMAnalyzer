"""Validate a symlink chain description for cycles and excessive length.

Agents report link chains as ``target -> next`` pairs without following
them on disk.  Detecting cycles offline prevents recursive copy jobs from
spinning forever when the reported graph is malformed.
"""

import logging
from typing import Dict, List, Optional

LOG = logging.getLogger(__name__)


def find_cycle(links: Dict[str, str], start: str) -> Optional[List[str]]:
    """Return the cycle path starting at *start*, or None when acyclic."""
    path: List[str] = []
    position: Dict[str, int] = {}
    cursor = start
    while cursor in links:
        if cursor in position:
            cycle = path[position[cursor]:] + [cursor]
            LOG.warning("symlink cycle detected: %s", " -> ".join(cycle))
            return cycle
        position[cursor] = len(path)
        path.append(cursor)
        cursor = links[cursor]
    return None


def chain_length(links: Dict[str, str], start: str, limit: int = 64) -> int:
    """Return the resolution depth, raising when the chain exceeds *limit*."""
    depth = 0
    seen = set()
    cursor = start
    while cursor in links:
        if cursor in seen:
            raise ValueError("cycle encountered from {!r}".format(start))
        seen.add(cursor)
        depth += 1
        if depth > limit:
            raise ValueError("symlink chain longer than {} steps".format(limit))
        cursor = links[cursor]
    LOG.debug("resolved %d symlink step(s) for %s", depth, start)
    return depth


__all__ = ["find_cycle", "chain_length"]
