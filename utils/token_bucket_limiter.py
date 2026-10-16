"""Token bucket rate limiting for outbound agent actions.

Smoothed API driven actions keep the agent from being rate limited upstream,
while a burst capacity still allows a short spike when it is genuinely needed.
"""
import time
import logging

LOG = logging.getLogger(__name__)


class TokenBucket:
    """Token bucket refilling at a steady rate up to a burst capacity."""

    def __init__(self, rate_per_sec, burst, now=None):
        if rate_per_sec <= 0 or burst <= 0:
            raise ValueError('rate and burst must be positive')
        self.rate = float(rate_per_sec)
        self.capacity = float(burst)
        self.tokens = float(burst)
        self.updated = now if now is not None else time.monotonic()

    def _refill(self, now):
        self.tokens = min(self.capacity, self.tokens + max(0.0, now - self.updated) * self.rate)
        self.updated = now

    def allow(self, cost=1.0, now=None):
        """Consume tokens when available and report whether the action may run."""
        moment = now if now is not None else time.monotonic()
        self._refill(moment)
        if self.tokens >= cost:
            self.tokens -= cost
            return True
        LOG.debug('rate limited with %.3f tokens available', self.tokens)
        return False


__all__ = ['TokenBucket']
