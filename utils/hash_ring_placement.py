"""Hash ring placement resolving keys to server nodes.

Each server is hashed to a position on a circular key space.  A key's owner is
the first server position at or after the key's hash, wrapping around at the
end, which keeps most assignments stable when servers are added or removed.
"""

import bisect
import hashlib
import logging
from typing import Dict, List, Sequence

LOG = logging.getLogger(__name__)


def hash_token(token: str) -> int:
    """Return a stable integer hash for *token*."""
    digest = hashlib.md5(token.encode("utf-8")).hexdigest()[:8]
    return int(digest, 16)


class HashRing:
    """Place keys on a ring of hashed server positions."""

    def __init__(self, servers: Sequence[str]) -> None:
        points: List[int] = []
        owners: List[str] = []
        for server in servers:
            points.append(hash_token(server))
            owners.append(server)
        order = sorted(range(len(points)), key=points.__getitem__)
        self._points = [points[index] for index in order]
        self._owners = [owners[index] for index in order]
        LOG.debug("built hash ring with %d points", len(self._points))

    def assign(self, key: str) -> str:
        """Return the server owning *key* on the ring."""
        if not self._points:
            raise ValueError("hash ring is empty")
        position = bisect.bisect(self._points, hash_token(key)) % len(self._points)
        return self._owners[position]

    def distribution(self, keys: Sequence[str]) -> Dict[str, int]:
        """Count how many keys map to each server."""
        counts: Dict[str, int] = {server: 0 for server in self._owners}
        for key in keys:
            counts[self.assign(key)] += 1
        return counts

    def __len__(self) -> int:
        return len(self._points)


__all__ = ["HashRing", "hash_token"]
