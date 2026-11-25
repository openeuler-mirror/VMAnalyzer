"""vhost worker thread utilisation estimate.

Saturated vhost workers bottleneck all virtio devices of a guest, so busy
cycles are compared against wall clock time per worker.
"""
import logging

LOG = logging.getLogger(__name__)


def utilisation(busy_ns, wall_ns):
    """Return the busy share of a worker in 0..1."""
    if not wall_ns or wall_ns <= 0:
        return 0.0
    return round(max(0.0, min(1.0, float(busy_ns) / float(wall_ns))), 3)


def saturated_workers(stats, watermark=0.85):
    """Return the names of workers above the utilisation watermark."""
    hot = []
    for name, pair in (stats or {}).items():
        busy, wall = pair[0], pair[1]
        if utilisation(busy, wall) >= watermark:
            hot.append(name)
    LOG.debug('%d saturated vhost workers', len(hot))
    return sorted(hot)


__all__ = ['utilisation', 'saturated_workers']
