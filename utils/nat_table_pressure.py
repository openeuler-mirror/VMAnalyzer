"""NAT table pressure estimation.

SNAT port allocation fails when the per destination port pool is exhausted,
so used ports are compared against the ephemeral range size.
"""
import logging

LOG = logging.getLogger(__name__)


def pool_usage(used_ports, range_start=32768, range_end=60999):
    """Return 0..1 usage of the source port pool."""
    size = max(1, int(range_end) - int(range_start))
    return round(max(0.0, min(1.0, float(used_ports) / float(size))), 3)


def exhaustion_eta(used_ports, rate_per_sec, range_start=32768, range_end=60999):
    """Return seconds until the pool is exhausted, or None."""
    if rate_per_sec <= 0:
        return None
    size = max(1, int(range_end) - int(range_start))
    gap = size - float(used_ports)
    if gap <= 0:
        return 0.0
    eta = gap / rate_per_sec
    LOG.debug('nat pool eta %.0fs', eta)
    return round(eta, 1)


__all__ = ['pool_usage', 'exhaustion_eta']
