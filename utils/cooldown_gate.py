"""Cooldown gate for repeated actions.

Allows an action only after a minimum quiet period has passed since the last
time it ran, preventing rapid flapping of a corrective action.
"""
from dataclasses import dataclass


@dataclass
class CooldownGate:
    """Track the last fire time and enforce a minimum spacing."""

    cooldown: float
    last_fired: float = None

    def ready(self, now):
        """Report whether the gate is open at the given time."""
        if self.last_fired is None:
            return True
        return now - self.last_fired >= self.cooldown

    def fire(self, now):
        """Open the gate if ready and record the fire time."""
        if not self.ready(now):
            return False
        self.last_fired = now
        return True

    def remaining(self, now):
        """Return the seconds until the gate next opens."""
        if self.ready(now):
            return 0.0
        return self.cooldown - (now - self.last_fired)


__all__ = ["CooldownGate"]
