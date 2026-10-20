"""Floyd-Warshall all-pairs shortest paths with next-hop reconstruction.

The triple loop relaxes every ordered pair through each intermediate vertex in
turn.  A companion next-hop matrix lets callers rebuild the actual route from
any source to any destination after the table is built.
"""

import logging
import math
from typing import List, Optional, Sequence, Tuple

LOG = logging.getLogger(__name__)

INF = math.inf


def floyd_warshall(matrix: Sequence[Sequence[float]]) -> Tuple[List[List[float]], List[List[Optional[int]]]]:
    """Return the distance table and the next-hop table for all pairs."""
    size = len(matrix)
    distance = [list(row) for row in matrix]
    hop = [[column if distance[row][column] != INF else None for column in range(size)]
           for row in range(size)]
    for middle in range(size):
        for start in range(size):
            if distance[start][middle] == INF:
                continue
            for end in range(size):
                candidate = distance[start][middle] + distance[middle][end]
                if candidate < distance[start][end]:
                    distance[start][end] = candidate
                    hop[start][end] = hop[start][middle]
    LOG.debug("computed all-pairs table for %d nodes", size)
    return distance, hop


def reconstruct_path(hop: Sequence[Sequence[Optional[int]]], start: int, end: int) -> Optional[List[int]]:
    """Rebuild the hop sequence from *start* to *end* when reachable."""
    if hop[start][end] is None:
        return None
    path = [start]
    while start != end:
        start = hop[start][end]
        path.append(start)
    return path


__all__ = ["floyd_warshall", "reconstruct_path", "INF"]
