"""Write a value into a nested mapping, creating intermediate levels.

Configuration overlays arrive as dotted key paths and must be applied onto
an existing tree.  Creating missing levels on demand avoids repetitive
guard code at every call site.
"""

import logging
from typing import Any, Dict, List, MutableMapping, Optional

LOG = logging.getLogger(__name__)


def set_path(tree: MutableMapping, dotted: str,
             value: Any, separator: str = ".") -> MutableMapping:
    """Assign *value* at the dotted path, creating nested mappings."""
    parts: List[str] = [part for part in dotted.split(separator) if part]
    if not parts:
        raise ValueError("path must contain at least one segment")
    cursor = tree
    for part in parts[:-1]:
        nxt = cursor.get(part)
        if not isinstance(nxt, MutableMapping):
            if nxt is not None:
                LOG.debug("replacing scalar at %r with a mapping", part)
            nxt = {}
            cursor[part] = nxt
        cursor = nxt
    cursor[parts[-1]] = value
    return tree


def merge_paths(tree: Optional[MutableMapping], updates: Dict[str, Any],
                separator: str = ".") -> Dict[str, Any]:
    """Apply a batch of dotted updates onto a copy of *tree*."""
    result: Dict[str, Any] = dict(tree or {})
    for path, value in updates.items():
        set_path(result, path, value, separator)
    return result


__all__ = ["set_path", "merge_paths"]
