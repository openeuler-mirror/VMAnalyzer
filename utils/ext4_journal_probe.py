"""ext4 journal transaction rate tracking.

A journal that commits too frequently amplifies write traffic, so commits and
bytes are combined into a wear indicator per interval.
"""
import logging

LOG = logging.getLogger(__name__)


def commit_rate(commits, interval_sec):
    """Return journal commits per second."""
    if not interval_sec or interval_sec <= 0:
        return 0.0
    return round(float(commits) / float(interval_sec), 3)


def wear_indicator(commits, bytes_written, commit_ceiling=200.0):
    """Return 0..1 wear indicator from commit pressure and volume."""
    pressure = min(1.0, float(commits) / commit_ceiling) if commit_ceiling else 0.0
    volume = min(1.0, float(bytes_written or 0) / float(1 << 30))
    score = round(0.6 * pressure + 0.4 * volume, 3)
    LOG.debug('ext4 journal wear %.3f', score)
    return score


__all__ = ['commit_rate', 'wear_indicator']
