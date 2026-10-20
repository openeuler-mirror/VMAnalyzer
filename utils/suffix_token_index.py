"""Substring search index built from sorted suffix offsets.

Each token in the corpus gets a list of suffixes sorted lexicographically.
Queries then binary search the sorted suffix list to collect matching tokens,
which keeps memory proportional to the corpus size rather than to all pairs.
"""

import bisect
import logging
from typing import List, Sequence

LOG = logging.getLogger(__name__)


def _suffixes(token: str) -> List[str]:
    return [token[i:] for i in range(len(token))]


class SuffixTokenIndex:
    """Map of sorted suffixes to the tokens that produced them."""

    def __init__(self, tokens: Sequence[str]) -> None:
        pairs: List[tuple] = []
        for token in tokens:
            for suffix in _suffixes(token):
                pairs.append((suffix, token))
        pairs.sort(key=lambda item: (item[0], item[1]))
        self._keys = [p[0] for p in pairs]
        self._values = [p[1] for p in pairs]
        LOG.debug("indexed %d suffixes", len(pairs))

    def containing(self, needle: str) -> List[str]:
        """Return unique tokens whose text contains *needle*."""
        if not needle:
            return []
        low = bisect.bisect_left(self._keys, needle)
        hits: List[str] = []
        seen: set = set()
        while low < len(self._keys) and self._keys[low].startswith(needle):
            token = self._values[low]
            if token not in seen:
                seen.add(token)
                hits.append(token)
            low += 1
        return hits


def count_matches(index: SuffixTokenIndex, needle: str) -> int:
    """Number of distinct tokens containing *needle*."""
    return len(index.containing(needle))


__all__ = ["SuffixTokenIndex", "count_matches"]
