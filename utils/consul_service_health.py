"""Consul service health tally.

A service is only routable when every check passes; tallying statuses per
service finds the ones with warning or critical checks.
"""
import logging

LOG = logging.getLogger(__name__)


def tally_checks(checks):
    """Return {status: count} for a list of check dicts."""
    tally = {}
    for check in checks or []:
        status = str(check.get('status', 'unknown'))
        tally[status] = tally.get(status, 0) + 1
    return tally


def is_routable(checks):
    """Return True only when every check is passing."""
    bad = [c for c in checks or [] if c.get('status') != 'passing']
    if bad:
        LOG.debug('service blocked by %d non-passing checks', len(bad))
    return not bad


__all__ = ['tally_checks', 'is_routable']
