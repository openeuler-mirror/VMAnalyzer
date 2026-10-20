"""Maximum bipartite matching using Kuhn augmenting paths.

For each left vertex the algorithm attempts to find an alternating path to an
unmatched right vertex, reassigning earlier matches when necessary.  This
lightweight variant returns the matching as a left-to-right dictionary.
"""

import logging
from typing import Dict, Hashable, List, Sequence

LOG = logging.getLogger(__name__)


def maximum_matching(left: Sequence[Hashable], adjacency: Dict) -> Dict:
    """Return a left-to-right matching of maximum cardinality."""
    match_right: Dict = {}

    def try_assign(node: Hashable, visited: set) -> bool:
        for candidate in adjacency.get(node, []):
            if candidate in visited:
                continue
            visited.add(candidate)
            if candidate not in match_right or try_assign(match_right[candidate], visited):
                match_right[candidate] = node
                return True
        return False

    for node in left:
        try_assign(node, set())
    result: Dict = {left_node: right for right, left_node in match_right.items()}
    LOG.debug("matched %d of %d left vertices", len(result), len(left))
    return result


def matching_size(left: Sequence[Hashable], adjacency: Dict) -> int:
    """Return the cardinality of a maximum matching."""
    return len(maximum_matching(left, adjacency))


def unmatched_left(left: Sequence[Hashable], adjacency: Dict) -> List[Hashable]:
    """Return left vertices left without a partner."""
    matched = maximum_matching(left, adjacency)
    return [node for node in left if node not in matched]


__all__ = ["maximum_matching", "matching_size", "unmatched_left"]
