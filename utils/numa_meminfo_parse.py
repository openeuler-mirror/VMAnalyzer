"""Parse ``virsh numatune`` memory placement output per node.

NUMA placement determines whether a guest pays remote access penalties.
Extracting the per-node memory mapping allows the collector to compute the
local share and flag guests pinned across nodes.
"""

import logging
import re
from typing import Dict, Iterable, Optional

LOG = logging.getLogger(__name__)

NODE_PATTERN = re.compile(r"node\s+(?P<node>\d+)\s+(?P<value>-?\d+)")


def parse_numa_nodes(lines: Iterable[str]) -> Dict[int, int]:
    """Return memory kilobytes per NUMA node."""
    nodes: Dict[int, int] = {}
    for line in lines:
        match = NODE_PATTERN.search(line)
        if not match:
            continue
        nodes[int(match.group("node"))] = int(match.group("value"))
    LOG.debug("parsed %d NUMA node(s)", len(nodes))
    return nodes


def local_share(nodes: Dict[int, int], local_node: Optional[int]) -> float:
    """Return the fraction of memory placed on the local node."""
    total = sum(value for value in nodes.values() if value > 0)
    if not total or local_node is None:
        return 0.0
    return round(max(0, nodes.get(local_node, 0)) / total, 4)


def spread_nodes(nodes: Dict[int, int], threshold: float = 0.9) -> bool:
    """Return True when no single node holds most of the memory."""
    total = sum(value for value in nodes.values() if value > 0)
    if not total:
        return False
    return max(nodes.values()) / total < threshold


__all__ = ["NODE_PATTERN", "parse_numa_nodes", "local_share", "spread_nodes"]
