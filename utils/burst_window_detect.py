"""Detect bursts inside a rolling time window.

Classifies a stream as bursty when the count of events inside any trailing
window exceeds a configured threshold.
"""
from collections import deque


def burst_windows(timestamps, window_seconds, threshold):
    """Return window end instants whose trailing count breaches threshold."""
    ordered = sorted(timestamps)
    active = deque()
    breaches = []
    for stamp in ordered:
        active.append(stamp)
        cutoff = stamp - window_seconds
        while active and active[0] < cutoff:
            active.popleft()
        if len(active) > threshold:
            breaches.append((stamp, len(active)))
    return breaches


def peak_in_window(timestamps, window_seconds):
    """Return the highest event count observed in any trailing window."""
    counts = [count for _, count in burst_windows(timestamps, window_seconds, -1)]
    return max(counts) if counts else 0


__all__ = ["burst_windows", "peak_in_window"]
