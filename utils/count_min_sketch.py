"""Count-Min sketch sizing.

Heavy hitters in log streams are found with a sketch whose width and depth
follow from the tolerated error and confidence.
"""
import logging
import math

LOG = logging.getLogger(__name__)


def dimensions(error, confidence):
    """Return (width, depth) for the tolerated error and confidence."""
    eps = max(1e-6, float(error or 0.001))
    delta = min(0.5, max(1e-6, 1.0 - float(confidence or 0.99)))
    width = int(math.ceil(math.e / eps))
    depth = int(math.ceil(math.log(1.0 / delta)))
    LOG.debug('cms %dx%d', width, depth)
    return width, depth


def memory_bytes(width, depth, counter_size=4):
    """Return the sketch memory footprint in bytes."""
    return int(width or 0) * int(depth or 0) * int(counter_size or 4)


__all__ = ['dimensions', 'memory_bytes']
