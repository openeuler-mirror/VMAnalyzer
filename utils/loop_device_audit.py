"""Loop device leak detection.

Forgotten loop devices pin deleted files and memory, so attached devices are
counted and compared against the number the workload legitimately needs.
"""
import logging

LOG = logging.getLogger(__name__)


def attached_count(loop_entries):
    """Count loop entries that carry a backing file."""
    return sum(1 for e in loop_entries or [] if (e or {}).get('backing_file'))


def leaked(attached, expected):
    """Report how many more devices are attached than expected."""
    extra = max(0, int(attached or 0) - int(expected or 0))
    if extra:
        LOG.warning('%d unexpected loop devices attached', extra)
    return extra


__all__ = ['attached_count', 'leaked']
