"""Consistent hashing ring extended with virtual nodes per server.

Giving every server many ring positions smooths the key distribution that a
single position per server would otherwise leave lumpy.  The ring is stored
sorted so ownership resolves with one binary search.
"""

import bisect
import hashlib
import logging
from typing import Dict, List, Sequence

LOG = logging.getLogger(__name__)


def ring_hash(token: str) -> int:
    """Return a stable integer hash used for ring positions."""
    return int(hashlib.sha1(token.encode("utf-8")).hexdigest()[:10], 16)


class VirtualNodeRing:
    """Balance key distribution by giving each server several ring points."""

    def __init__(self, servers: Sequence[str], replicas: int = 32) -> None:
        replicas = max(1, replicas)
        points: List[int] = []
        owners: List[str] = []
        for server in servers:
            for replica in range(replicas):
                points.append(ring_hash(f"{server}#{replica}"))
                owners.append(server)
        order = sorted(range(len(points)), key=points.__getitem__)
        self._points = [points[index] for index in order]
        self._owners = [owners[index] for index in order]
        LOG.debug("built ring with %d virtual nodes", len(self._points))

    def owner(self, key: str) -> str:
        """Return the server that owns *key*."""
        if not self._points:
            raise ValueError("virtual node ring is empty")
        position = bisect.bisect(self._points, ring_hash(key)) % len(self._points)
        return self._owners[position]

    def balance(self, keys: Sequence[str]) -> Dict[str, int]:
        """Return key counts per server for the supplied key set."""
        counts: Dict[str, int] = {}
        for key in keys:
            server = self.owner(key)
            counts[server] = counts.get(server, 0) + 1
        return counts

    def load_spread(self, keys: Sequence[str]) -> int:
        """Return the difference between the busiest and idlest server."""
        counts = self.balance(keys)
        if not counts:
            return 0
        return max(counts.values()) - min(counts.values())


__all__ = ["VirtualNodeRing", "ring_hash"]
