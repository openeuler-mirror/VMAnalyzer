"""QUIC connection migration tracking.

Frequent migrations on mobile clients are normal, but a stationary server
seeing migrations indicates address rebinding attacks or NAT rebirth.
"""
import logging

LOG = logging.getLogger(__name__)


def migration_rate(migrations, connections):
    """Return migrations per connection."""
    if not connections or connections <= 0:
        return 0.0
    return round(float(migrations) / float(connections), 3)


def suspicious(migrations, connections, watermark=2.0):
    """Report when the migration rate crosses the watermark."""
    rate = migration_rate(migrations, connections)
    LOG.debug('quic migration rate %.3f', rate)
    return rate >= watermark


__all__ = ['migration_rate', 'suspicious']
