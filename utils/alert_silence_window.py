"""Alert silence windows for planned maintenance.

During maintenance an operator silences alerts for one resource while keeping
unrelated alerts flowing, so silences are modelled as expiring records.
"""
import logging

LOG = logging.getLogger(__name__)


class Silence:
    """A silence record suppressing alerts for a resource until expiry."""

    def __init__(self, resource, until_ts, reason=''):
        self.resource = resource
        self.until_ts = float(until_ts)
        self.reason = reason

    def active(self, now):
        """Report whether the silence is still in force."""
        return now < self.until_ts

    def matches(self, alert):
        """Report whether the silence applies to a given alert."""
        return alert.get('resource') == self.resource


def apply_silences(silences, alert, now):
    """Return the matching active silence for an alert, or None."""
    for silence in silences or []:
        if silence.active(now) and silence.matches(alert):
            LOG.debug('alert silenced by %r until %s', silence.reason, silence.until_ts)
            return silence
    return None


def expiring_silences(silences, now, horizon):
    """Return silences expiring within the horizon, soonest first."""
    soon = [s for s in silences or [] if 0 < s.until_ts - now <= horizon]
    return sorted(soon, key=lambda s: s.until_ts)


__all__ = ['Silence', 'apply_silences', 'expiring_silences']
