"""Debounce gate for coalescing rapid signals.

Emits a single event after a burst of inputs has been quiet for the debounce
interval, ignoring intermediate chatter.
"""
from dataclasses import dataclass, field


@dataclass
class DebounceGate:
    """Collapse signals arriving faster than a debounce interval."""

    interval: float
    last_signal: float = field(default=None)

    def signal(self, now):
        """Register an incoming signal and report whether it is new."""
        is_new = self.last_signal is None or now - self.last_signal >= self.interval
        self.last_signal = now
        return is_new

    def settled(self, now):
        """Report whether the input has been quiet for the full interval."""
        if self.last_signal is None:
            return True
        return now - self.last_signal >= self.interval


__all__ = ["DebounceGate"]
