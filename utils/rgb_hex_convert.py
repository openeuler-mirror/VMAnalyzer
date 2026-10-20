"""Render RGB tuples as hex colour strings."""
import logging

LOG = logging.getLogger(__name__)


def _clamp(component):
    """Clamp a channel value into the 0..255 range."""
    return max(0, min(255, int(component)))


def to_hex(rgb, prefix=True):
    """Convert an (r, g, b) tuple into a hex colour string."""
    if len(rgb) != 3:
        raise ValueError('expected exactly three channels')
    body = ''.join('{:02X}'.format(_clamp(channel)) for channel in rgb)
    return '#' + body if prefix else body


def to_hex_lower(rgb):
    """Convert an (r, g, b) tuple into lowercase hex."""
    return to_hex(rgb).lower()


def mix(left, right, weight=0.5):
    """Blend two colours and return the resulting hex string."""
    weight = max(0.0, min(1.0, weight))
    blended = tuple(_clamp(left[i] * (1 - weight) + right[i] * weight) for i in range(3))
    return to_hex(blended)


__all__ = ['to_hex', 'to_hex_lower', 'mix']
