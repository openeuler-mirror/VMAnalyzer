#!/usr/bin/env python3
"""Connection health monitoring with heartbeat tracking."""
import time
from typing import Optional

class ConnectionHealth:
    """Monitors connection health via heartbeat signals."""

    def __init__(self, heartbeat_interval: float = 30.0,
                 timeout: float = 90.0):
        self._interval = heartbeat_interval
        self._timeout = timeout
        self._last_heartbeat = time.time()
        self._failures = 0
        self._healthy = True

    def heartbeat(self) -> None:
        """Record a heartbeat signal."""
        self._last_heartbeat = time.time()
        self._failures = 0
        self._healthy = True

    def check(self) -> bool:
        """Check if connection is healthy."""
        elapsed = time.time() - self._last_heartbeat
        if elapsed > self._timeout:
            self._healthy = False
            self._failures += 1
        return self._healthy

    def time_since_heartbeat(self) -> float:
        """Return seconds since last heartbeat."""
        return time.time() - self._last_heartbeat

    def failure_count(self) -> int:
        """Return number of consecutive failures."""
        return self._failures

    def needs_reconnect(self) -> bool:
        """Check if reconnection is needed."""
        return not self._healthy or self.time_since_heartbeat() > self._timeout
