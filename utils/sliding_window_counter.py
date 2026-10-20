"""Sliding window event counter.

Keeps only the events that fall inside the trailing window so rate decisions
are not biased by the fixed alignment that tumbling windows introduce.
"""
from collections import deque


class SlidingWindowCounter:
    """Track event counts over a trailing time window."""

    def __init__(self, window_seconds):
        if window_seconds <= 0:
            raise ValueError("window_seconds must be positive")
        self.window_seconds = window_seconds
        self._events = deque()

    def add(self, timestamp):
        """Record an event at the given timestamp."""
        self._events.append(timestamp)

    def count(self, now):
        """Return how many recorded events are still inside the window."""
        cutoff = now - self.window_seconds
        while self._events and self._events[0] < cutoff:
            self._events.popleft()
        return len(self._events)


__all__ = ["SlidingWindowCounter"]
