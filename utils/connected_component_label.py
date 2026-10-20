"""Two-pass connected-component labelling for binary grids.

The first pass assigns provisional labels and records merges between
neighbouring foreground cells.  The second pass resolves provisional labels to
final component numbers, which is the classic approach used in image analysis.
"""

import logging
from typing import Dict, List, Sequence

LOG = logging.getLogger(__name__)

Grid = Sequence[Sequence[int]]


def label_components(grid: Grid) -> List[List[int]]:
    """Assign component ids to 4-connected non-zero grid cells."""
    rows = len(grid)
    columns = len(grid[0]) if rows else 0
    labels = [[0] * columns for _ in range(rows)]
    parent: List[int] = [0]

    def find(value: int) -> int:
        while parent[value] != value:
            parent[value] = parent[parent[value]]
            value = parent[value]
        return value

    def union(first: int, second: int) -> None:
        root_first, root_second = find(first), find(second)
        if root_first != root_second:
            parent[max(root_first, root_second)] = min(root_first, root_second)

    counter = 0
    for row in range(rows):
        for column in range(columns):
            if not grid[row][column]:
                continue
            neighbours = []
            if row > 0 and labels[row - 1][column]:
                neighbours.append(labels[row - 1][column])
            if column > 0 and labels[row][column - 1]:
                neighbours.append(labels[row][column - 1])
            if not neighbours:
                counter += 1
                parent.append(counter)
                labels[row][column] = counter
            else:
                labels[row][column] = min(neighbours)
                for other in neighbours:
                    union(labels[row][column], other)
    roots: Dict[int, int] = {}
    for row in range(rows):
        for column in range(columns):
            if labels[row][column]:
                root = find(labels[row][column])
                roots.setdefault(root, len(roots) + 1)
                labels[row][column] = roots[root]
    LOG.debug("labelled %d components", len(roots))
    return labels


def count_components(grid: Grid) -> int:
    """Return how many distinct non-zero components the grid holds."""
    labels = label_components(grid)
    return len({value for row in labels for value in row} - {0})


__all__ = ["label_components", "count_components"]
