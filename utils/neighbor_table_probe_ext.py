"""IPv6 neighbour table pressure.

The neighbour table has a hard kernel limit; proximity to that limit causes
intermittent unreachability that is hard to debug.
"""
import logging

LOG = logging.getLogger(__name__)


def fill_ratio(entries, gc_thresh3=1024):
    """Return entries divided by the hard threshold."""
    if gc_thresh3 <= 0:
        return 0.0
    return round(max(0.0, min(1.0, float(entries) / float(gc_thresh3))), 3)


def state_histogram(states):
    """Return {state: count} for neighbour entries."""
    hist = {}
    for state in states or []:
        key = str(state).upper()
        hist[key] = hist.get(key, 0) + 1
    LOG.debug('neighbour states %s', hist)
    return hist


__all__ = ['fill_ratio', 'state_histogram']
