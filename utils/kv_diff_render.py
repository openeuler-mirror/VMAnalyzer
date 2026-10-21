"""Render differences between two key-value snapshots as text lines.

Comparing configuration snapshots is a routine troubleshooting step.  A
stable, readable diff output works better than raw dict printing because it
shows additions, removals and changes separately.
"""

import logging
from typing import Dict, List

LOG = logging.getLogger(__name__)


def diff(before: Dict[str, object], after: Dict[str, object]) -> Dict[str, List[str]]:
    """Return added, removed and changed keys."""
    before_keys, after_keys = set(before), set(after)
    changed = sorted(key for key in before_keys & after_keys if before[key] != after[key])
    result = {
        "added": sorted(after_keys - before_keys),
        "removed": sorted(before_keys - after_keys),
        "changed": changed,
    }
    LOG.debug("diff has %d addition(s), %d removal(s), %d change(s)",
              len(result["added"]), len(result["removed"]), len(result["changed"]))
    return result


def render(before: Dict[str, object], after: Dict[str, object]) -> List[str]:
    """Render a diff as prefixed text lines."""
    changes = diff(before, after)
    lines: List[str] = []
    for key in changes["added"]:
        lines.append("+ {} = {}".format(key, after[key]))
    for key in changes["removed"]:
        lines.append("- {} = {}".format(key, before[key]))
    for key in changes["changed"]:
        lines.append("~ {}: {} -> {}".format(key, before[key], after[key]))
    return lines


def is_empty(before: Dict[str, object], after: Dict[str, object]) -> bool:
    """Return True when the snapshots are identical."""
    return not any(diff(before, after).values())


__all__ = ["diff", "render", "is_empty"]
