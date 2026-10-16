"""Log severity distribution analysis.

Reading only the error count hides a service that is mostly warning.  These
helpers build a severity histogram and compute the error share so the shape of
the log stream is visible at a glance.
"""
import logging

LOG = logging.getLogger(__name__)

LEVELS = ('debug', 'info', 'warning', 'error', 'critical')


def histogram(entries):
    """Count log entries per severity level."""
    counts = {level: 0 for level in LEVELS}
    for entry in entries or []:
        level = str(entry.get('level', '')).lower()
        if level not in counts:
            LOG.debug('unknown level %r counted as info', level)
            level = 'info'
        counts[level] += 1
    return counts


def error_share(counts):
    """Return the combined error and critical share of all entries."""
    total = sum(counts.values())
    if total == 0:
        return 0.0
    bad = counts.get('error', 0) + counts.get('critical', 0)
    return round(bad / float(total), 4)


def dominant_level(counts):
    """Return the severity level holding the most entries."""
    if not counts:
        return None
    return max(counts, key=lambda level: counts[level])


__all__ = ['histogram', 'error_share', 'dominant_level']
