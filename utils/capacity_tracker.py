#!/usr/bin/env python3
"""Track resource capacity utilization for VM hosts."""
from typing import Dict, Optional

class CapacityTracker:
    """Tracks allocated vs total capacity for resources."""

    def __init__(self):
        self._resources: Dict[str, dict] = {}

    def register(self, resource: str, total: float) -> None:
        """Register a resource with total capacity."""
        self._resources[resource] = {"total": total, "allocated": 0.0}

    def allocate(self, resource: str, amount: float) -> bool:
        """Allocate capacity from a resource."""
        if resource not in self._resources:
            return False
        r = self._resources[resource]
        if r["allocated"] + amount > r["total"]:
            return False
        r["allocated"] += amount
        return True

    def release(self, resource: str, amount: float) -> None:
        """Release allocated capacity."""
        if resource in self._resources:
            self._resources[resource]["allocated"] = max(
                0, self._resources[resource]["allocated"] - amount)

    def utilization(self, resource: str) -> Optional[float]:
        """Return utilization ratio (0-1)."""
        if resource not in self._resources:
            return None
        r = self._resources[resource]
        return r["allocated"] / r["total"] if r["total"] > 0 else 0.0

    def available(self, resource: str) -> Optional[float]:
        """Return available capacity."""
        if resource not in self._resources:
            return None
        r = self._resources[resource]
        return r["total"] - r["allocated"]
