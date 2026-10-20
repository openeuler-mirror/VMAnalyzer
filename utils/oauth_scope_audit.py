"""OAuth scope grant audit.

Clients should hold only the scopes they requested; diffing granted
against requested scopes surfaces privilege creep.
"""
import logging

LOG = logging.getLogger(__name__)
DANGEROUS = {'admin', 'write:all', 'delete:any'}


def scope_diff(requested, granted):
    """Return (missing, extra) scope sets."""
    req, got = set(requested or []), set(granted or [])
    return (sorted(req - got), sorted(got - req))


def dangerous_grants(granted):
    """Return granted scopes on the dangerous list."""
    bad = sorted(set(granted or []) & DANGEROUS)
    if bad:
        LOG.debug('dangerous scopes granted %s', bad)
    return bad


__all__ = ['scope_diff', 'dangerous_grants', 'DANGEROUS']
