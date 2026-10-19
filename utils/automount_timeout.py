"""Automount idle timeout tuning.

Short idle timeouts cause repeated mount storms on busy hierarchies, so the
observed mount rate is compared against the timeout.
"""
import logging

LOG = logging.getLogger(__name__)


def mounts_per_hour(mount_events, window_sec):
    """Return the automount event rate per hour."""
    if not window_sec or window_sec <= 0:
        return 0.0
    return round(3600.0 * float(mount_events or 0) / float(window_sec), 2)


def suggest_timeout(rate_per_hour):
    """Suggest an idle timeout in seconds based on the mount rate."""
    if rate_per_hour >= 120:
        suggestion = 600
    elif rate_per_hour >= 30:
        suggestion = 300
    else:
        suggestion = 60
    LOG.debug('automount rate %.1f/h -> %ds', rate_per_hour, suggestion)
    return suggestion


__all__ = ['mounts_per_hour', 'suggest_timeout']
