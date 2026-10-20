"""Token bucket refill arithmetic.

Separates the pure maths of refilling tokens from any wall clock access so the
policy can be unit tested with synthetic timestamps.
"""
import logging

LOG = logging.getLogger(__name__)


def refill_tokens(tokens, rate, elapsed, capacity):
    """Return the token count after refilling for elapsed seconds."""
    if rate < 0 or capacity <= 0:
        raise ValueError("rate must be non negative and capacity positive")
    filled = tokens + max(0.0, elapsed) * rate
    return min(float(capacity), filled)


def can_consume(tokens, cost):
    """Report whether the bucket currently affords the requested cost."""
    return tokens >= cost


def drain(tokens, cost):
    """Return the remaining tokens after spending cost, if affordable."""
    if not can_consume(tokens, cost):
        return None
    return tokens - cost


__all__ = ["refill_tokens", "can_consume", "drain"]
