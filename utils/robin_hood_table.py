"""Robin Hood hash probe distance.

Balanced tables keep probe distances tight; the maximum distance bounds the
worst-case lookup.
"""
import logging

LOG = logging.getLogger(__name__)


def max_probe_distance(probe_distances):
    """Return the longest probe sequence in the table."""
    vals = [int(d) for d in probe_distances or [] if d is not None]
    dist = max(vals) if vals else 0
    LOG.debug('robin hood max probe %d', dist)
    return dist


def variance(probe_distances):
    """Return the variance of probe distances, a balance indicator."""
    vals = [float(d) for d in probe_distances or [] if d is not None]
    if not vals:
        return 0.0
    mean = sum(vals) / len(vals)
    return round(sum((v - mean) ** 2 for v in vals) / len(vals), 3)


__all__ = ['max_probe_distance', 'variance']
