"""CFS bandwidth throttling detection for cgroup backed guests.

When a guest exceeds its cpu.max quota the kernel throttles its runqueue.  A
rising throttled period ratio means the workload is being starved by policy
rather than by physical capacity.
"""
from dataclasses import dataclass


@dataclass
class ThrottleWindow:
    """One observation of cgroup CFS bandwidth counters."""

    periods: int
    throttled: int
    throttled_us: int

    def ratio(self):
        """Return the throttled period ratio in the 0..1 range."""
        if self.periods <= 0:
            return 0.0
        return min(1.0, self.throttled / float(self.periods))

    def average_throttle_us(self):
        """Return the average throttle duration per throttled period."""
        if self.throttled <= 0:
            return 0.0
        return self.throttled_us / float(self.throttled)


def detect_throttling(window, ratio_limit=0.2):
    """Report whether a window breaches the tolerated throttle ratio."""
    ratio = window.ratio()
    return {
        'ratio': round(ratio, 4),
        'throttled': ratio > ratio_limit,
        'severity': 'high' if ratio > 0.5 else 'low' if ratio > ratio_limit else 'none',
    }


def worst_window(windows):
    """Pick the window with the highest throttle ratio."""
    if not windows:
        return None
    return max(windows, key=lambda w: w.ratio())


__all__ = ['ThrottleWindow', 'detect_throttling', 'worst_window']
