"""TLS protocol version audit.

Legacy protocol versions weaken the whole fleet, so negotiated versions are
counted and flagged against the minimum policy.
"""
import logging
from collections import Counter

LOG = logging.getLogger(__name__)

ORDER = ['SSLv3', 'TLSv1.0', 'TLSv1.1', 'TLSv1.2', 'TLSv1.3']


def count_versions(negotiated):
    """Return {version: count} for negotiated connections."""
    return dict(Counter(str(v) for v in negotiated or []))


def below_policy(negotiated, minimum='TLSv1.2'):
    """Return connections negotiated below the minimum version."""
    floor = ORDER.index(minimum) if minimum in ORDER else 0
    bad = [v for v in negotiated or [] if str(v) in ORDER and ORDER.index(str(v)) < floor]
    LOG.debug('%d connections below %s', len(bad), minimum)
    return bad


__all__ = ['count_versions', 'below_policy']
