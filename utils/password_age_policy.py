"""Password age policy check.

Privileged accounts rotate faster; age in days is compared against the
role-specific maximum.
"""
import logging

LOG = logging.getLogger(__name__)

ROLE_MAX_AGE = {'admin': 60, 'service': 90, 'user': 180}


def age_days(changed_ts, now_ts):
    """Return whole days since the password changed."""
    return max(0, int((float(now_ts or 0) - float(changed_ts or 0)) / 86400.0))


def overdue(role, changed_ts, now_ts):
    """Report when the password outlived the role maximum."""
    limit = ROLE_MAX_AGE.get(str(role or 'user'), 180)
    over = age_days(changed_ts, now_ts) > limit
    if over:
        LOG.warning('%s password overdue', role)
    return over


__all__ = ['age_days', 'overdue']
