"""Radix map that compacts single-child chains into labelled edges.

Contiguous keys that share a long stem are stored as one edge label instead
of one node per character.  This module exposes insertion and the longest
common prefix scan used when compressing routing tables or file paths.
"""

import logging
from typing import Dict, List, Tuple

LOG = logging.getLogger(__name__)


class RadixMap:
    """Edge-labelled prefix map with implicit chain compaction."""

    def __init__(self) -> None:
        self._table: Dict[str, int] = {}

    def add(self, key: str, weight: int = 1) -> None:
        """Insert *key* merging it into any existing prefix bucket."""
        merged = False
        for existing in list(self._table):
            common = longest_common_prefix(existing, key)
            if common != len(existing):
                continue
            if common == len(existing):
                self._table[existing] += weight
                merged = True
            break
        if not merged:
            self._table[key] = self._table.get(key, 0) + weight

    def buckets(self) -> List[Tuple[str, int]]:
        """Return the compacted edge labels together with their weights."""
        return sorted(self._table.items())

    def prefix_hits(self, prefix: str) -> List[str]:
        """Edge labels that begin with *prefix*."""
        return [label for label, _ in self.buckets() if label.startswith(prefix)]


def longest_common_prefix(left: str, right: str) -> int:
    """Length of the shared leading run of *left* and *right*."""
    limit = min(len(left), len(right))
    index = 0
    while index < limit and left[index] == right[index]:
        index += 1
    LOG.debug("lcp=%d for pair", index)
    return index


def compress(labels: List[str]) -> int:
    """Number of distinct edge labels remaining after compaction."""
    return len({label for label in labels})


__all__ = ["RadixMap", "longest_common_prefix", "compress"]
