"""Index the positions of each token in a token stream.

Log correlation needs to jump from a suspicious token to every occurrence
in a captured buffer.  A single pass builds the index so repeated lookups
over the same payload stay cheap.
"""

import logging
from typing import Dict, Iterable, List, Sequence

LOG = logging.getLogger(__name__)


def build_index(tokens: Sequence[str]) -> Dict[str, List[int]]:
    """Map each token to the sorted list of its positions."""
    index: Dict[str, List[int]] = {}
    for position, token in enumerate(tokens):
        index.setdefault(token, []).append(position)
    LOG.debug("indexed %d token(s) with %d distinct values", len(tokens), len(index))
    return index


def positions_of(index: Dict[str, List[int]], token: str) -> List[int]:
    """Return positions for *token*, or an empty list when absent."""
    return index.get(token, [])


def nearest(index: Dict[str, List[int]], token: str, target: int) -> int:
    """Return the position of *token* closest to *target*, or -1."""
    candidates = index.get(token, [])
    if not candidates:
        return -1
    return min(candidates, key=lambda position: abs(position - target))


def window_hits(index: Dict[str, List[int]], tokens: Iterable[str],
                start: int, end: int) -> Dict[str, int]:
    """Count occurrences of each token inside ``[start, end)``."""
    counts: Dict[str, int] = {}
    for token in tokens:
        counts[token] = sum(1 for position in index.get(token, []) if start <= position < end)
    return counts


__all__ = ["build_index", "positions_of", "nearest", "window_hits"]
