#!/usr/bin/env python3
"""Quota enforcer for resource usage limits."""
from typing import Dict, Optional, List, Callable
from dataclasses import dataclass, field
from collections import defaultdict
import time
import threading

@dataclass
class Quota:
    resource: str
    limit: float
    used: float = 0.0
    window: float = 3600.0
    reset_time: float = field(default_factory=time.time)
    overflow_count: int = 0

class QuotaEnforcer:
    def __init__(self, default_window: float = 3600.0):
        self._quotas: Dict[str, Dict[str, Quota]] = defaultdict(dict)
        self._default_window = default_window
        self._lock = threading.Lock()
        self._callbacks: List[Callable] = []
        self._running = False

    def set_quota(self, tenant: str, resource: str,
                  limit: float, window: Optional[float] = None) -> Quota:
        with self._lock:
            quota = Quota(
                resource=resource, limit=limit,
                window=window or self._default_window
            )
            self._quotas[tenant][resource] = quota
            return quota

    def check(self, tenant: str, resource: str, amount: float = 1.0) -> bool:
        with self._lock:
            quota = self._quotas.get(tenant, {}).get(resource)
            if not quota:
                return True
            self._reset_if_needed(quota)
            return quota.used + amount <= quota.limit

    def consume(self, tenant: str, resource: str,
                amount: float = 1.0) -> bool:
        with self._lock:
            quota = self._quotas.get(tenant, {}).get(resource)
            if not quota:
                return True
            self._reset_if_needed(quota)
            if quota.used + amount > quota.limit:
                quota.overflow_count += 1
                self._fire("overflow", tenant, resource, quota)
                return False
            quota.used += amount
            if quota.used >= quota.limit * 0.9:
                self._fire("warning", tenant, resource, quota)
            return True

    def release(self, tenant: str, resource: str, amount: float = 1.0) -> None:
        with self._lock:
            quota = self._quotas.get(tenant, {}).get(resource)
            if quota:
                quota.used = max(0, quota.used - amount)

    def _reset_if_needed(self, quota: Quota) -> None:
        now = time.time()
        if now - quota.reset_time >= quota.window:
            quota.used = 0
            quota.reset_time = now
            quota.overflow_count = 0

    def get_usage(self, tenant: str, resource: str) -> Optional[Dict]:
        with self._lock:
            quota = self._quotas.get(tenant, {}).get(resource)
            if not quota:
                return None
            self._reset_if_needed(quota)
            return {
                "resource": quota.resource,
                "limit": quota.limit,
                "used": quota.used,
                "remaining": max(0, quota.limit - quota.used),
                "utilization": quota.used / quota.limit if quota.limit > 0 else 0,
                "overflow_count": quota.overflow_count,
                "window": quota.window,
            }

    def get_tenant_quotas(self, tenant: str) -> List[Dict]:
        with self._lock:
            quotas = self._quotas.get(tenant, {})
            return [self.get_usage(tenant, r) for r in quotas if quotas[r]]

    def remove_quota(self, tenant: str, resource: str) -> bool:
        with self._lock:
            return self._quotas.get(tenant, {}).pop(resource, None) is not None

    def on_event(self, callback: Callable) -> None:
        self._callbacks.append(callback)

    def _fire(self, event: str, tenant: str,
              resource: str, quota: Quota) -> None:
        for cb in self._callbacks:
            try:
                cb(event, tenant, resource, quota)
            except Exception:
                pass

    @property
    def tenant_count(self) -> int:
        with self._lock:
            return len(self._quotas)
