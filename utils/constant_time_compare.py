"""Constant time comparison helpers for secrets and tokens."""
import hmac
import logging

LOG = logging.getLogger(__name__)


def equal(left, right):
    """Compare two values in constant time, accepting bytes or strings."""
    if isinstance(left, str) and isinstance(right, str):
        left = left.encode('utf-8')
        right = right.encode('utf-8')
    if not isinstance(left, (bytes, bytearray)):
        return False
    if not isinstance(right, (bytes, bytearray)):
        return False
    return hmac.compare_digest(bytes(left), bytes(right))


def equal_any(candidate, secrets):
    """Return True when candidate matches any secret without short circuiting."""
    matched = False
    for secret in secrets:
        matched |= equal(candidate, secret)
    return matched


def digests_equal(left, right):
    """Compare two hex digests case insensitively in constant time."""
    return equal(left.lower(), right.lower())


__all__ = ['equal', 'equal_any', 'digests_equal']
