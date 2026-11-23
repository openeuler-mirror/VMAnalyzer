"""Socket buffer memory pressure.

When socket buffers approach their cgroup or system limit the kernel starts
dropping; pressure is the used fraction of the configured ceiling.
"""
import logging

LOG = logging.getLogger(__name__)


def pressure(used_bytes, limit_bytes):
    """Return 0..1 usage of socket buffer memory."""
    if not limit_bytes or limit_bytes <= 0:
        return 0.0
    return round(max(0.0, min(1.0, float(used_bytes) / float(limit_bytes))), 3)


def recommendation(used_bytes, limit_bytes, warn=0.8):
    """Return a new limit suggestion when pressure is high, else None."""
    if pressure(used_bytes, limit_bytes) < warn:
        return None
    suggested = int(float(limit_bytes) * 2)
    LOG.debug('suggest skbuff limit %d', suggested)
    return suggested


__all__ = ['pressure', 'recommendation']
