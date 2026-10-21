"""Measure how deeply a path sits below a reference directory.

Backup tools need a bounded copy depth to avoid runaway recursive directories
such as accidental mounts.  This helper reports depth without touching the
filesystem so it can run on path lists collected from agents.
"""

import logging
import posixpath
from typing import Dict, List, Optional

LOG = logging.getLogger(__name__)


def relative_depth(path: str, root: Optional[str] = None) -> int:
    """Return the number of components below *root* (or the path itself)."""
    normalised = posixpath.normpath(path)
    if root:
        root_normalised = posixpath.normpath(root)
        if not normalised.startswith(root_normalised.rstrip("/") + "/"):
            return -1
        normalised = normalised[len(root_normalised.rstrip("/")) + 1:]
    parts = [part for part in normalised.split("/") if part and part != "."]
    return len(parts)


def depth_report(paths: List[str], root: Optional[str] = None) -> Dict[str, object]:
    """Summarise depth statistics for a batch of paths."""
    depths = [relative_depth(path, root) for path in paths]
    valid = [depth for depth in depths if depth >= 0]
    report = {
        "total": len(paths),
        "outside_root": len(paths) - len(valid),
        "max_depth": max(valid) if valid else 0,
        "mean_depth": round(sum(valid) / len(valid), 2) if valid else 0.0,
    }
    LOG.debug("depth report %s", report)
    return report


__all__ = ["relative_depth", "depth_report"]
