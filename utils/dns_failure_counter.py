"""DNS failure classification.

NXDOMAIN storms and SERVFAIL loops have different owners, so failures are
counted per rcode instead of lumped together.
"""
import logging
from collections import Counter

LOG = logging.getLogger(__name__)


def count_by_rcode(rcodes):
    """Return {rcode: count} with unknown rcodes grouped as OTHER."""
    known = {'NOERROR', 'NXDOMAIN', 'SERVFAIL', 'REFUSED', 'FORMERR'}
    counts = Counter()
    for code in rcodes or []:
        key = str(code).upper()
        counts[key if key in known else 'OTHER'] += 1
    return dict(counts)


def failure_ratio(counts):
    """Return non NOERROR responses divided by all responses."""
    total = sum((counts or {}).values())
    if total == 0:
        return 0.0
    bad = total - counts.get('NOERROR', 0)
    LOG.debug('dns failure ratio %d/%d', bad, total)
    return round(bad / float(total), 4)


__all__ = ['count_by_rcode', 'failure_ratio']
