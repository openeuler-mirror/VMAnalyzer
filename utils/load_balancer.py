#!/usr/bin/env python3
"""Load balancer with multiple distribution strategies."""
from typing import List, Dict, Any, Optional, Callable
from enum import Enum
import random
import time
import threading
from collections import defaultdict

class BalancingStrategy(Enum):
    ROUND_ROBIN = "round_robin"
    RANDOM = "random"
    LEAST_CONNECTIONS = "least_connections"
    WEIGHTED = "weighted"
    IP_HASH = "ip_hash"

class Backend:
    def __init__(self, name: str, address: str, weight: int = 1):
        self._name = name
        self._address = address
        self._weight = weight
        self._healthy = True
        self._connections = 0
        self._total_requests = 0
        self._total_errors = 0
        self._last_check = time.time()

    @property
    def name(self) -> str:
        return self._name

    @property
    def address(self) -> str:
        return self._address

    @property
    def weight(self) -> int:
        return self._weight

    @property
    def healthy(self) -> bool:
        return self._healthy

    @property
    def connections(self) -> int:
        return self._connections

    def set_healthy(self, healthy: bool) -> None:
        self._healthy = healthy
        self._last_check = time.time()

    def increment_connections(self) -> None:
        self._connections += 1
        self._total_requests += 1

    def decrement_connections(self) -> None:
        self._connections = max(0, self._connections - 1)

    def record_error(self) -> None:
        self._total_errors += 1

    def stats(self) -> Dict[str, Any]:
        return {
            "name": self._name,
            "address": self._address,
            "healthy": self._healthy,
            "connections": self._connections,
            "total_requests": self._total_requests,
            "total_errors": self._total_errors,
            "error_rate": self._total_errors / max(1, self._total_requests),
        }

class LoadBalancer:
    def __init__(self, strategy: BalancingStrategy = BalancingStrategy.ROUND_ROBIN):
        self._strategy = strategy
        self._backends: List[Backend] = []
        self._rr_index = 0
        self._lock = threading.Lock()
        self._ip_hash_map: Dict[str, Backend] = {}
        self._health_check_interval = 30.0
        self._health_check_func: Optional[Callable] = None
        self._running = False
        self._health_thread: Optional[threading.Thread] = None

    def add_backend(self, backend: Backend) -> None:
        with self._lock:
            self._backends.append(backend)

    def remove_backend(self, name: str) -> bool:
        with self._lock:
            for i, b in enumerate(self._backends):
                if b.name == name:
                    self._backends.pop(i)
                    return True
            return False

    def get_backend(self, client_id: str = "") -> Optional[Backend]:
        with self._lock:
            healthy = [b for b in self._backends if b.healthy]
            if not healthy:
                return None
            if self._strategy == BalancingStrategy.ROUND_ROBIN:
                backend = healthy[self._rr_index % len(healthy)]
                self._rr_index += 1
            elif self._strategy == BalancingStrategy.RANDOM:
                backend = random.choice(healthy)
            elif self._strategy == BalancingStrategy.LEAST_CONNECTIONS:
                backend = min(healthy, key=lambda b: b.connections)
            elif self._strategy == BalancingStrategy.WEIGHTED:
                weights = [b.weight for b in healthy]
                backend = random.choices(healthy, weights=weights)[0]
            elif self._strategy == BalancingStrategy.IP_HASH:
                if client_id and client_id in self._ip_hash_map:
                    if self._ip_hash_map[client_id].healthy:
                        backend = self._ip_hash_map[client_id]
                    else:
                        backend = healthy[hash(client_id) % len(healthy)]
                        self._ip_hash_map[client_id] = backend
                else:
                    backend = healthy[hash(client_id) % len(healthy)]
                    self._ip_hash_map[client_id] = backend
            else:
                backend = healthy[0]
            backend.increment_connections()
            return backend

    def release_backend(self, backend: Backend, error: bool = False) -> None:
        backend.decrement_connections()
        if error:
            backend.record_error()

    def set_strategy(self, strategy: BalancingStrategy) -> None:
        with self._lock:
            self._strategy = strategy

    def set_health_check(self, func: Callable) -> None:
        self._health_check_func = func

    def start_health_checks(self, interval: float = 30.0) -> None:
        self._health_check_interval = interval
        self._running = True
        self._health_thread = threading.Thread(target=self._health_loop, daemon=True)
        self._health_thread.start()

    def stop_health_checks(self) -> None:
        self._running = False
        if self._health_thread:
            self._health_thread.join(timeout=5)

    def _health_loop(self) -> None:
        while self._running:
            if self._health_check_func:
                for backend in self._backends:
                    try:
                        healthy = self._health_check_func(backend)
                        backend.set_healthy(healthy)
                    except Exception:
                        backend.set_healthy(False)
            time.sleep(self._health_check_interval)

    def get_stats(self) -> Dict[str, Any]:
        return {
            "strategy": self._strategy.value,
            "backend_count": len(self._backends),
            "healthy_count": sum(1 for b in self._backends if b.healthy),
            "backends": [b.stats() for b in self._backends],
        }

    def list_backends(self) -> List[str]:
        return [b.name for b in self._backends]

    def backend_count(self) -> int:
        return len(self._backends)
