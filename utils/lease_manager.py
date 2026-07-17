#!/usr/bin/env python3
"""Time-based resource lease management."""
import time
from typing import Dict, List, Optional

class LeaseManager:
    """Manages time-limited leases on resources."""

    def __init__(self):
        self._leases: Dict[str, dict] = {}

    def acquire(self, resource: str, holder: str,
                duration: float = 3600.0) -> str:
        """Acquire a lease on a resource."""
        lease_id = f"{resource}_{holder}_{int(time.time())}"
        self._leases[lease_id] = {
            "resource": resource,
            "holder": holder,
            "expires": time.time() + duration,
        }
        return lease_id

    def release(self, lease_id: str) -> bool:
        """Release a lease."""
        if lease_id in self._leases:
            del self._leases[lease_id]
            return True
        return False

    def is_valid(self, lease_id: str) -> bool:
        """Check if a lease is still valid."""
        if lease_id not in self._leases:
            return False
        return time.time() < self._leases[lease_id]["expires"]

    def expire_leases(self) -> int:
        """Remove expired leases and return count."""
        now = time.time()
        expired = [lid for lid, l in self._leases.items() if now >= l["expires"]]
        for lid in expired:
            del self._leases[lid]
        return len(expired)

    def list_leases(self, resource: str = None) -> List[str]:
        """List active lease IDs, optionally filtered by resource."""
        self.expire_leases()
        if resource:
            return [lid for lid, l in self._leases.items() if l["resource"] == resource]
        return list(self._leases.keys())
