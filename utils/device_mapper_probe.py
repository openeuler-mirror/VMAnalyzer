"""Device mapper target health.

dm targets report their status strings; any status other than a plain active
form means the mapping needs attention.
"""
import logging

LOG = logging.getLogger(__name__)


def healthy_targets(status_lines):
    """Count targets whose status string starts with 'active'."""
    return sum(1 for line in status_lines or [] if str(line).strip().startswith('active'))


def degraded_targets(status_lines):
    """Return the names of targets that are not active."""
    bad = []
    for line in status_lines or []:
        parts = str(line).split(':', 1)
        if len(parts) == 2 and not parts[1].strip().startswith('active'):
            bad.append(parts[0].strip())
    if bad:
        LOG.warning('dm degraded targets %s', bad)
    return bad


__all__ = ['healthy_targets', 'degraded_targets']
