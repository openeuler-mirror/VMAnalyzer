"""SPICE channel accounting.

Each display channel carries its own traffic; a channel with zero bytes since
connect is a broken session rather than an idle one.
"""
import logging

LOG = logging.getLogger(__name__)


def idle_channels(channels, min_bytes=1):
    """Return channel names that transferred less than min_bytes."""
    idle = [name for name, b in (channels or {}).items() if int(b) < min_bytes]
    LOG.debug('%d idle spice channels', len(idle))
    return sorted(idle)


def channel_share(channels):
    """Return {channel: share_of_total_bytes}."""
    total = sum(int(b) for b in (channels or {}).values())
    if total <= 0:
        return {}
    return {name: round(int(b) / float(total), 3) for name, b in channels.items()}


__all__ = ['idle_channels', 'channel_share']
