"""Debounce filter that collapses a flurry of repeated events.

When a device flaps it can emit dozens of identical alerts within seconds;
keeping only the first and counting the rest keeps the agent output readable.
"""
import logging

LOG = logging.getLogger(__name__)


class Debouncer:
    """Timestamped gate that suppresses repeats within a quiet window."""

    def __init__(self, window_sec):
        if window_sec <= 0:
            raise ValueError('window must be positive')
        self.window = float(window_sec)
        self.last_seen = {}
        self.suppressed = {}

    def accept(self, key, now):
        """Return True when the key is new or the window has elapsed."""
        moment = float(now)
        previous = self.last_seen.get(key)
        if previous is not None and moment - previous < self.window:
            self.suppressed[key] = self.suppressed.get(key, 0) + 1
            return False
        self.last_seen[key] = moment
        return True

    def drain(self, key):
        """Return and reset the number of events suppressed for a key."""
        count = self.suppressed.pop(key, 0)
        self.last_seen.pop(key, None)
        return count


def debounce_events(events, window_sec):
    """Filter an iterable of (key, timestamp) pairs, returning kept events."""
    gate = Debouncer(window_sec)
    kept = []
    total = 0
    for key, now in events or []:
        total += 1
        if gate.accept(key, now):
            kept.append((key, now))
    LOG.debug('debounce kept %d of %d events', len(kept), total)
    return kept


__all__ = ['Debouncer', 'debounce_events']
