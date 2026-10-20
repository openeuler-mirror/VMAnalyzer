"""Interval overlap queries backed by an augmented balanced-ish tree.

Intervals are stored in a binary search tree keyed on the low endpoint and
augmented with the maximum high endpoint in each subtree.  A query prunes
whole subtrees when their maximum endpoint sits below the probe start.
"""

import logging
from dataclasses import dataclass
from typing import List, Optional

LOG = logging.getLogger(__name__)


@dataclass
class Node:
    """Tree node holding one interval and subtree maximum."""

    low: int
    high: int
    max_end: int
    left: Optional["Node"] = None
    right: Optional["Node"] = None


def _update(node: Node) -> None:
    best = node.high
    if node.left is not None:
        best = max(best, node.left.max_end)
    if node.right is not None:
        best = max(best, node.right.max_end)
    node.max_end = best


def insert(root: Optional[Node], low: int, high: int) -> Node:
    """Insert the interval ``[low, high)`` keyed by its start."""
    if root is None:
        return Node(low, high, high)
    if low < root.low:
        root.left = insert(root.left, low, high)
    else:
        root.right = insert(root.right, low, high)
    _update(root)
    return root


def overlaps(root: Optional[Node], qlow: int, qhigh: int) -> List[tuple]:
    """Return every stored interval intersecting the probe range."""
    found: List[tuple] = []
    stack = [root]
    while stack:
        node = stack.pop()
        if node is None or node.max_end <= qlow:
            continue
        if node.low < qhigh and node.high > qlow:
            found.append((node.low, node.high))
        if node.left is not None:
            stack.append(node.left)
        stack.append(node.right)
    LOG.debug("probe returned %d intervals", len(found))
    return found


__all__ = ["Node", "insert", "overlaps"]
