#!/usr/bin/env python3
"""Countdown latch for thread synchronization."""
import threading

class AsyncLatch:
    """A countdown latch that waits for N threads to complete."""

    def __init__(self, count: int = 1):
        self._count = count
        self._condition = threading.Condition()

    def count_down(self) -> None:
        """Decrement the countdown."""
        with self._condition:
            self._count = max(0, self._count - 1)
            if self._count == 0:
                self._condition.notify_all()

    def wait(self, timeout: float = None) -> bool:
        """Wait for countdown to reach zero."""
        with self._condition:
            if self._count == 0:
                return True
            return self._condition.wait_for(
                lambda: self._count == 0, timeout=timeout)

    @property
    def count(self) -> int:
        """Return current countdown value."""
        with self._condition:
            return self._count

    def reset(self, count: int) -> None:
        """Reset the latch to a new count."""
        with self._condition:
            self._count = count
