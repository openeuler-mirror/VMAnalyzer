"""Session idle timeout decisions.

Tracks the last activity instant of a session and decides whether it has idled
beyond its timeout, optionally granting a warning grace period.
"""
from dataclasses import dataclass


@dataclass
class Session:
    """A session identified by token with a last seen timestamp."""

    token: str
    last_seen: float

    def idle_seconds(self, now):
        """Return how long the session has been idle."""
        return max(0.0, now - self.last_seen)

    def is_idle(self, now, timeout):
        """Report whether the session exceeded its idle timeout."""
        return self.idle_seconds(now) > timeout

    def is_warning(self, now, timeout, grace):
        """Report whether the session is inside the warning grace band."""
        idle = self.idle_seconds(now)
        return timeout < idle <= timeout + grace


def idle_sessions(sessions, now, timeout):
    """Return the tokens of sessions that have idled out."""
    return [s.token for s in sessions if s.is_idle(now, timeout)]


__all__ = ["Session", "idle_sessions"]
