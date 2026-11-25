"""SYN flood guard heuristics.

A SYN rate that dwarfs the completion rate indicates spoofed sources; the
ratio drives the guard decision.
"""
import logging

LOG = logging.getLogger(__name__)


def completion_ratio(syns, established):
    """Return established per received SYN."""
    if not syns or syns <= 0:
        return 1.0
    return round(min(1.0, float(established) / float(syns)), 3)


def is_flood(syns, established, watermark=0.3):
    """Report when the completion ratio drops below the watermark."""
    ratio = completion_ratio(syns, established)
    if ratio < watermark and syns > 100:
        LOG.debug('syn flood ratio %.3f over %d syns', ratio, syns)
        return True
    return False


__all__ = ['completion_ratio', 'is_flood']
