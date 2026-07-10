#!/usr/bin/env python3
"""Service mesh sidecar proxy for traffic management."""
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field
from collections import defaultdict
import time
import threading
from enum import Enum

class RouteStrategy(Enum):
    ROUND_ROBIN = "round_robin"
    RANDOM = "random"
    WEIGHTED = "weighted"
    LEAST_CONN = "least_conn"

@dataclass
class UpstreamService:
    name: str
    host: str
    port: int
    weight: int = 1
    healthy: bool = True
    active_connections: int = 0
    total_requests: int = 0
    error_count: int = 0

@dataclass
class RouteRule:
    match_path: str
    match_method: str = "*"
    upstream: str = ""
    strategy: RouteStrategy = RouteStrategy.ROUND_ROBIN
    timeout: float = 30.0
    retry_count: int = 2

class SidecarProxy:
    def __init__(self, service_name: str):
        self._service_name = service_name
        self._upstreams: Dict[str, List[UpstreamService]] = defaultdict(list)
        self._routes: List[RouteRule] = []
        self._rr_index: Dict[str, int] = defaultdict(int)
        self._lock = threading.Lock()
        self._middleware: List[Callable] = []
        self._stats = {
            "total_requests": 0, "success": 0,
            "errors": 0, "retries": 0, "timeouts": 0
        }

    def add_upstream(self, group: str, service: UpstreamService) -> None:
        with self._lock:
            self._upstreams[group].append(service)

    def add_route(self, rule: RouteRule) -> None:
        with self._lock:
            self._routes.append(rule)

    def add_middleware(self, middleware: Callable) -> None:
        self._middleware.append(middleware)

    def route(self, path: str, method: str = "GET") -> Optional[UpstreamService]:
        with self._lock:
            rule = self._match_route(path, method)
            if not rule:
                return None
            upstreams = [u for u in self._upstreams[rule.upstream] if u.healthy]
            if not upstreams:
                return None
            self._stats["total_requests"] += 1
            return self._select_upstream(rule, upstreams)

    def _match_route(self, path: str, method: str) -> Optional[RouteRule]:
        for rule in self._routes:
            if path.startswith(rule.match_path):
                if rule.match_method == "*" or method == rule.match_method:
                    return rule
        return None

    def _select_upstream(self, rule: RouteRule,
                         upstreams: List[UpstreamService]) -> UpstreamService:
        if rule.strategy == RouteStrategy.ROUND_ROBIN:
            idx = self._rr_index[rule.upstream] % len(upstreams)
            self._rr_index[rule.upstream] += 1
            return upstreams[idx]
        elif rule.strategy == RouteStrategy.LEAST_CONN:
            return min(upstreams, key=lambda u: u.active_connections)
        elif rule.strategy == RouteStrategy.WEIGHTED:
            total = sum(u.weight for u in upstreams)
            import random
            r = random.randint(1, total)
            for u in upstreams:
                r -= u.weight
                if r <= 0:
                    return u
            return upstreams[0]
        else:
            import random
            return random.choice(upstreams)

    def record_success(self, upstream: UpstreamService) -> None:
        with self._lock:
            upstream.total_requests += 1
            upstream.active_connections = max(0, upstream.active_connections - 1)
            self._stats["success"] += 1

    def record_error(self, upstream: UpstreamService) -> None:
        with self._lock:
            upstream.error_count += 1
            upstream.active_connections = max(0, upstream.active_connections - 1)
            self._stats["errors"] += 1
            if upstream.error_count > 5:
                upstream.healthy = False

    def mark_healthy(self, group: str, host: str, port: int) -> None:
        with self._lock:
            for u in self._upstreams[group]:
                if u.host == host and u.port == port:
                    u.healthy = True
                    u.error_count = 0

    @property
    def stats(self) -> Dict[str, Any]:
        with self._lock:
            return dict(self._stats)

    def upstream_stats(self) -> Dict[str, List[Dict]]:
        with self._lock:
            return {
                group: [
                    {"host": u.host, "port": u.port, "healthy": u.healthy,
                     "weight": u.weight, "requests": u.total_requests,
                     "errors": u.error_count,
                     "active": u.active_connections}
                    for u in services
                ]
                for group, services in self._upstreams.items()
            }
