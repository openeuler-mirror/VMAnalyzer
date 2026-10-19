"""HTTP redirect chain audit.

Long redirect chains waste round trips and often hide a misconfigured vhost,
so chain lengths are validated against a hop budget.
"""
import logging

LOG = logging.getLogger(__name__)

HOP_STATUSES = {301, 302, 303, 307, 308}


def chain_length(statuses):
    """Return the number of redirect hops in a status sequence."""
    return sum(1 for s in statuses or [] if int(s) in HOP_STATUSES)


def detect_loop(locations):
    """Return the first repeated Location, proving a redirect loop."""
    seen = set()
    for loc in locations or []:
        key = str(loc)
        if key in seen:
            LOG.debug('redirect loop at %s', key)
            return key
        seen.add(key)
    return None


__all__ = ['chain_length', 'detect_loop']
