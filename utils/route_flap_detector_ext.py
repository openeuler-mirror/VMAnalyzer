"""Route flap detection.

A route that changes repeatedly within minutes blackholes traffic on and off,
so change intervals per prefix are scored.
"""
import logging

LOG = logging.getLogger(__name__)


def flap_score(timestamps):
    """Return the number of changes inside the shortest 10 minute window."""
    stamps = sorted(float(t) for t in timestamps or [])
    best = 0
    for i, start in enumerate(stamps):
        count = sum(1 for t in stamps[i:] if t - start <= 600.0)
        best = max(best, count)
    return best


def flapping_prefixes(events, threshold=5):
    """Return prefixes whose flap score crosses the threshold."""
    hot = []
    for prefix, stamps in (events or {}).items():
        if flap_score(stamps) >= threshold:
            hot.append(prefix)
    LOG.debug('%d flapping prefixes', len(hot))
    return sorted(hot)


__all__ = ['flap_score', 'flapping_prefixes']
