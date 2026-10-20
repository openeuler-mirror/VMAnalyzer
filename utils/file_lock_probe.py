"""File lock contention survey.

POSIX and flock locks serialise writers; the locked-file count and the oldest
waiter age surface stuck processes.
"""
import logging

LOG = logging.getLogger(__name__)


def contended_files(lock_rows):
    """Count files that have at least one blocked waiter."""
    return sum(1 for r in lock_rows or [] if (r or {}).get('blocked'))


def oldest_waiter_age(lock_rows, now_ts):
    """Return the age in seconds of the oldest blocked lock."""
    ages = []
    for r in lock_rows or []:
        if (r or {}).get('blocked') and r.get('since_ts') is not None:
            ages.append(max(0.0, float(now_ts or 0) - float(r['since_ts'])))
    age = max(ages) if ages else 0.0
    LOG.debug('oldest lock waiter %.1fs', age)
    return age


__all__ = ['contended_files', 'oldest_waiter_age']
