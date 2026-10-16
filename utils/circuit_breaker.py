"""Circuit breaker protecting the agent from a failing dependency.

Repeated failures open the breaker so the agent fails fast instead of queueing
timed out calls, and a probe request closes it again once the dependency
recovers.
"""
from dataclasses import dataclass
import logging

LOG = logging.getLogger(__name__)

STATE_CLOSED = 'closed'
STATE_OPEN = 'open'
STATE_HALF_OPEN = 'half_open'


@dataclass
class CircuitBreaker:
    """Failure counting breaker with an open and half open state machine."""

    failure_limit: int = 5
    recover_after: float = 30.0
    failures: int = 0
    state: str = STATE_CLOSED
    opened_at: float = 0.0

    def record_failure(self, now):
        """Record a failure and open the breaker once the limit is reached."""
        self.failures += 1
        if self.failures >= self.failure_limit:
            self.state = STATE_OPEN
            self.opened_at = now
            LOG.warning('circuit opened after %d failures', self.failures)

    def record_success(self):
        """Reset the failure counter and close the breaker."""
        self.failures = 0
        self.state = STATE_CLOSED


def allows_request(breaker, now):
    """Return whether a request may proceed under the current breaker state."""
    if breaker.state == STATE_CLOSED:
        return True
    if breaker.state == STATE_OPEN and now - breaker.opened_at >= breaker.recover_after:
        breaker.state = STATE_HALF_OPEN
        return True
    return breaker.state == STATE_HALF_OPEN


__all__ = ['CircuitBreaker', 'allows_request', 'STATE_CLOSED', 'STATE_OPEN', 'STATE_HALF_OPEN']
