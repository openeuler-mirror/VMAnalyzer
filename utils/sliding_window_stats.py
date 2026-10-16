"""Sliding window statistics over a streamed metric.

Keeping only the live window bounds memory while still providing mean, spread
and range for a continuously sampled metric.
"""
from collections import deque
import statistics
import logging

LOG = logging.getLogger(__name__)


class SlidingWindow:
    """Fixed capacity window that evicts the oldest sample first."""

    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError('capacity must be positive')
        self.samples = deque(maxlen=capacity)

    def push(self, value):
        """Append one sample to the window."""
        self.samples.append(float(value))

    def stats(self):
        """Return count, mean, spread and range of the current window."""
        if not self.samples:
            LOG.debug('window is empty')
            return {'count': 0}
        values = list(self.samples)
        return {
            'count': len(values),
            'mean': round(statistics.fmean(values), 4),
            'spread': round(statistics.pstdev(values), 4),
            'range': round(max(values) - min(values), 4),
        }


__all__ = ['SlidingWindow']
