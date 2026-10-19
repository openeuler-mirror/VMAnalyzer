"""Deficit round robin counters.

DRR gives each queue a byte budget per round; leftover deficit carries to the
next round so small packets are not starved.
"""
import logging

LOG = logging.getLogger(__name__)


def charge(deficit, packet_bytes):
    """Return remaining deficit after charging a packet."""
    return int(deficit or 0) - int(packet_bytes or 0)


def can_send(deficit, packet_bytes, quantum):
    """Report whether the queue may send the next packet."""
    allowed = int(deficit or 0) + int(quantum or 0) >= int(packet_bytes or 0)
    LOG.debug('drr send allowed=%s', allowed)
    return allowed


__all__ = ['charge', 'can_send']
