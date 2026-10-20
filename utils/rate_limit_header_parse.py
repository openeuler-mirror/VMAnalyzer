"""Rate limit header parsing.

X-RateLimit headers tell clients how much budget remains and when the
window resets; parsing them avoids blind retries.
"""
import logging
import time

LOG = logging.getLogger(__name__)


def parse_headers(headers):
    """Return {limit, remaining, reset} from a header dict."""
    lower = {str(k).lower(): v for k, v in (headers or {}).items()}
    return {
        'limit': int(lower.get('x-ratelimit-limit', 0)),
        'remaining': int(lower.get('x-ratelimit-remaining', 0)),
        'reset': int(lower.get('x-ratelimit-reset', 0)),
    }


def seconds_to_reset(headers, now=None):
    """Return seconds until the window resets, clamped at zero."""
    now = time.time() if now is None else now
    wait = max(0, int(parse_headers(headers)['reset'] - now))
    LOG.debug('rate limit resets in %ds', wait)
    return wait


__all__ = ['parse_headers', 'seconds_to_reset']
