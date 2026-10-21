"""Measure snapshot chain depth from disk backing references.

Deep chains slow down every write because each layer must be traversed.
Reporting depth and the deepest chain lets storage teams schedule merges
before performance degrades.
"""

import logging
from typing import Dict, List, Tuple

LOG = logging.getLogger(__name__)


def build_chain(backing: Dict[str, str]) -> Tuple[str, List[str]]:
    """Return the deepest chain root and its ordered members."""
    depths: Dict[str, int] = {}
    chains: Dict[str, List[str]] = {}

    def walk(node: str, seen: set) -> int:
        if node in depths:
            return depths[node]
        parent = backing.get(node)
        if parent is None or parent in seen:
            depths[node] = 1
            chains[node] = [node]
            return 1
        depth = walk(parent, seen | {node}) + 1
        depths[node] = depth
        chains[node] = chains.get(parent, [parent]) + [node]
        return depth

    for node in backing:
        walk(node, set())
    if not depths:
        return "", []
    root = max(depths, key=lambda item: depths[item])
    LOG.debug("deepest snapshot chain has %d layer(s)", depths[root])
    return root, chains.get(root, [])


def max_depth(backing: Dict[str, str]) -> int:
    """Return the number of layers in the deepest chain."""
    _, chain = build_chain(backing)
    return len(chain)


def suspicious(backing: Dict[str, str], limit: int = 8) -> List[str]:
    """Return leaf files whose chain exceeds *limit* layers."""
    leaves = set(backing) - set(backing.values())
    flagged = []
    for leaf in leaves:
        depth = 1
        cursor = leaf
        while cursor in backing:
            cursor = backing[cursor]
            depth += 1
            if depth > limit:
                flagged.append(leaf)
                break
    if flagged:
        LOG.warning("%d snapshot chain(s) exceed %d layers", len(flagged), limit)
    return flagged


__all__ = ["build_chain", "max_depth", "suspicious"]
