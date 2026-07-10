#!/usr/bin/env python3
"""Health check monitor for service status."""
from typing import Dict, List, Callable, Any, Optional
from enum import Enum
import time
import threading

class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"

class HealthCheck:
    def __init__(self, name: str, check_func: Callable[[], bool],
                 timeout: float = 5.0, critical: bool = True):
        self._name = name
        self._func = check_func
        self._timeout = timeout
        self._critical = critical
        self._status = HealthStatus.UNKNOWN
        self._last_check: Optional[float] = None
        self._last_error: Optional[str] = None
        self._consecutive_failures = 0

    @property
    def name(self) -> str:
        return self._name

    @property
    def status(self) -> HealthStatus:
        return self._status

    @property
    def critical(self) -> bool:
        return self._critical

    @property
    def last_error(self) -> Optional[str]:
        return self._last_error

    def run(self) -> HealthStatus:
        start = time.time()
        try:
            result = self._func()
            elapsed = time.time() - start
            if result:
                self._status = HealthStatus.HEALTHY
                self._consecutive_failures = 0
                self._last_error = None
            else:
                self._status = HealthStatus.UNHEALTHY
                self._consecutive_failures += 1
                self._last_error = "Check returned False"
        except Exception as e:
            self._status = HealthStatus.UNHEALTHY
            self._consecutive_failures += 1
            self._last_error = str(e)
        self._last_check = time.time()
        return self._status

    @property
    def last_check_time(self) -> Optional[float]:
        return self._last_check

    @property
    def consecutive_failures(self) -> int:
        return self._consecutive_failures

class HealthMonitor:
    def __init__(self, check_interval: float = 30.0):
        self._checks: Dict[str, HealthCheck] = {}
        self._interval = check_interval
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        self._callbacks: List[Callable] = []

    def add_check(self, check: HealthCheck) -> None:
        self._checks[check.name] = check

    def remove_check(self, name: str) -> bool:
        with self._lock:
            return self._checks.pop(name, None) is not None

    def check_now(self, name: str) -> Optional[HealthStatus]:
        check = self._checks.get(name)
        if check:
            status = check.run()
            self._notify(status, check)
            return status
        return None

    def check_all(self) -> Dict[str, HealthStatus]:
        results = {}
        with self._lock:
            checks = list(self._checks.values())
        for check in checks:
            status = check.run()
            results[check.name] = status
            self._notify(status, check)
        return results

    def overall_status(self) -> HealthStatus:
        if not self._checks:
            return HealthStatus.UNKNOWN
        has_unhealthy = False
        has_degraded = False
        for check in self._checks.values():
            if check.status == HealthStatus.UNHEALTHY and check.critical:
                return HealthStatus.UNHEALTHY
            if check.status == HealthStatus.UNHEALTHY:
                has_unhealthy = True
            if check.status == HealthStatus.DEGRADED:
                has_degraded = True
        if has_unhealthy:
            return HealthStatus.DEGRADED
        if has_degraded:
            return HealthStatus.DEGRADED
        return HealthStatus.HEALTHY

    def start(self) -> None:
        self._running = True
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)

    def _monitor_loop(self) -> None:
        while self._running:
            self.check_all()
            time.sleep(self._interval)

    def add_callback(self, callback: Callable) -> None:
        self._callbacks.append(callback)

    def _notify(self, status: HealthStatus, check: HealthCheck) -> None:
        for cb in self._callbacks:
            try:
                cb(status, check)
            except Exception:
                pass

    def get_status(self) -> Dict[str, Any]:
        return {
            "overall": self.overall_status().value,
            "checks": {name: {
                "status": c.status.value,
                "critical": c.critical,
                "last_error": c.last_error,
                "failures": c.consecutive_failures,
            } for name, c in self._checks.items()}
        }

    def check_count(self) -> int:
        return len(self._checks)
