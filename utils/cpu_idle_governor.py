"""CPU idle governor residency.

Deep C-states save power but cost wake latency; residency per state shows the
governor's choice.
"""
import logging

LOG = logging.getLogger(__name__)


def residency_share(state_us, total_us):
    """Return the share of idle time spent in one C-state."""
    if not total_us or total_us <= 0:
        return 0.0
    return round(min(1.0, float(state_us or 0) / float(total_us)), 3)


def deepest_state(shares):
    """Return the deepest C-state name holding at least ten percent."""
    order = sorted((shares or {}).items())
    deep = None
    for name, share in order:
        if float(share or 0) >= 0.1:
            deep = name
    LOG.debug('deepest used state %s', deep)
    return deep


__all__ = ['residency_share', 'deepest_state']
