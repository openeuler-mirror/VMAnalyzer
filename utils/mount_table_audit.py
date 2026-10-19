"""Mount table growth tracking.

Containers and bind mounts inflate /proc/mounts without bound on some hosts,
so entry counts are tracked against a host specific ceiling.
"""
import logging

LOG = logging.getLogger(__name__)


def entry_growth(prev_count, cur_count):
    """Return the delta of mount entries between polls."""
    return int(cur_count or 0) - int(prev_count or 0)


def over_ceiling(cur_count, ceiling=2000):
    """Report when the mount table grew past the ceiling."""
    over = int(cur_count or 0) > ceiling
    if over:
        LOG.warning('mount table has %s entries', cur_count)
    return over


__all__ = ['entry_growth', 'over_ceiling']
