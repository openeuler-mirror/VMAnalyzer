"""Numerically stable online mean and variance via Welford's method."""
import logging

LOG = logging.getLogger(__name__)


class RunningStats:
    """Accumulate mean and variance in one pass without storing samples."""

    def __init__(self):
        self.count = 0
        self.mean = 0.0
        self.m2 = 0.0

    def push(self, value):
        """Fold one sample into the running statistics."""
        self.count += 1
        delta = float(value) - self.mean
        self.mean += delta / self.count
        self.m2 += delta * (float(value) - self.mean)

    def variance(self, population=True):
        """Return the accumulated population or sample variance."""
        if self.count < 2:
            return 0.0
        divisor = self.count if population else self.count - 1
        return self.m2 / divisor

    def stddev(self):
        """Return the accumulated population standard deviation."""
        return self.variance() ** 0.5


def online_variance(values):
    """Return the population variance of values in a single pass."""
    stats = RunningStats()
    for value in values or []:
        stats.push(value)
    return stats.variance()


__all__ = ['RunningStats', 'online_variance']
