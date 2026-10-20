"""Directed cycle detection using depth-first search colouring.

Nodes move from white to grey on entry and to black on exit.  Encountering a
grey node means the search has stepped back onto the current recursion stack,
which exposes exactly one directed cycle for reporting.
"""

import logging
from collections import defaultdict
from typing import Dict, Iterable, List, Tuple

LOG = logging.getLogger(__name__)

WHITE, GREY, BLACK = 0, 1, 2


def find_cycle(nodes: Iterable[str], edges: Iterable[Tuple[str, str]]) -> List[str]:
    """Return one directed cycle as a node list, or an empty list."""
    adjacency: Dict[str, List[str]] = defaultdict(list)
    for source, target in edges:
        adjacency[source].append(target)
    colour: Dict[str, int] = {node: WHITE for node in nodes}
    path: List[str] = []

    def visit(node: str) -> List[str]:
        colour[node] = GREY
        path.append(node)
        for target in adjacency[node]:
            state = colour.get(target, WHITE)
            if state == WHITE:
                found = visit(target)
                if found:
                    return found
            elif state == GREY:
                start = path.index(target)
                return path[start:] + [target]
        path.pop()
        colour[node] = BLACK
        return []

    for node in list(colour):
        if colour[node] == WHITE:
            cycle = visit(node)
            if cycle:
                LOG.debug("cycle detected: %s", cycle)
                return cycle
    return []


def has_cycle(nodes: Iterable[str], edges: Iterable[Tuple[str, str]]) -> bool:
    """Return whether the directed graph contains any cycle."""
    return bool(find_cycle(nodes, edges))


__all__ = ["find_cycle", "has_cycle", "WHITE", "GREY", "BLACK"]
