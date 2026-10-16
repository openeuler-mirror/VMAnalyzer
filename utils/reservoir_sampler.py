"""Reservoir sampling for bounded metric retention.

Keeping a uniform sample of an unbounded stream avoids memory growth while still
giving statistically fair estimates of the underlying distribution.
"""
import random
import logging

LOG = logging.getLogger(__name__)


class ReservoirSampler:
    """Fixed size uniform sampler over an unbounded value stream."""

    def __init__(self, capacity, seed=None):
        if capacity <= 0:
            raise ValueError('capacity must be positive')
        self.capacity = capacity
        self.samples = []
        self.seen = 0
        self.rng = random.Random(seed)

    def offer(self, value):
        """Offer a value, accepting it with a decreasing probability."""
        self.seen += 1
        if len(self.samples) < self.capacity:
            self.samples.append(value)
            return True
        index = self.rng.randrange(self.seen)
        if index < self.capacity:
            self.samples[index] = value
            return True
        return False

    def mean(self):
        """Return the mean of the retained sample, or None when empty."""
        if not self.samples:
            LOG.debug('sampler has not retained any value')
            return None
        return round(sum(float(v) for v in self.samples) / len(self.samples), 4)


__all__ = ['ReservoirSampler']
