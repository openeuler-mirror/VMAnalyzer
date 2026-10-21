"""Render a nested path mapping as an ASCII directory tree.

Report archives and collected artefacts are naturally hierarchical.
Printing them as a tree makes missing branches obvious compared with a flat
sorted list of paths.
"""

import logging
from typing import Dict, List

LOG = logging.getLogger(__name__)


def build_tree(paths: List[str]) -> Dict[str, dict]:
    """Build a nested mapping from slash separated paths."""
    root: Dict[str, dict] = {}
    for path in paths:
        parts = [part for part in path.replace("\\", "/").split("/") if part]
        cursor = root
        for part in parts:
            cursor = cursor.setdefault(part, {})
    return root


def render(paths: List[str]) -> List[str]:
    """Return ASCII tree lines for the supplied paths."""
    tree = build_tree(paths)
    lines: List[str] = []

    def walk(node: Dict[str, dict], prefix: str) -> None:
        names = sorted(node)
        for index, name in enumerate(names):
            last = index == len(names) - 1
            connector = "`-- " if last else "|-- "
            lines.append(prefix + connector + name)
            walk(node[name], prefix + ("    " if last else "|   "))

    walk(tree, "")
    LOG.debug("rendered tree with %d line(s)", len(lines))
    return lines


__all__ = ["build_tree", "render"]
