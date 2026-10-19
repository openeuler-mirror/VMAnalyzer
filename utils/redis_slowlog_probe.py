"""Redis SLOWLOG triage.

Slowlog entries carry microsecond durations; counting entries above a
budget per command name shows which pattern hurts latency.
"""
import logging

LOG = logging.getLogger(__name__)


def over_budget(entries, budget_us=10000):
    """Return entries whose duration exceeds budget_us."""
    return [e for e in entries or [] if int(e.get('duration_us', 0)) > budget_us]


def by_command(entries):
    """Return {command: count} histogram of slow entries."""
    hist = {}
    for entry in entries or []:
        cmd = str(entry.get('command', '')).split(' ')[0].upper() or 'UNKNOWN'
        hist[cmd] = hist.get(cmd, 0) + 1
    LOG.debug('slowlog histogram %s', hist)
    return hist


__all__ = ['over_budget', 'by_command']
