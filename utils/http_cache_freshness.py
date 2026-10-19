"""HTTP cache freshness calculation.

A cached response is fresh while its age stays under the max-age from
Cache-Control; this helper computes the remaining lifetime.
"""
import logging

LOG = logging.getLogger(__name__)


def max_age_of(cache_control):
    """Return max-age seconds from a Cache-Control header, or 0."""
    for part in str(cache_control).split(','):
        part = part.strip()
        if part.startswith('max-age='):
            try:
                return int(part.split('=', 1)[1])
            except ValueError:
                return 0
    return 0


def is_fresh(cache_control, age_sec):
    """Return True while age stays under max-age."""
    lifetime = max_age_of(cache_control)
    fresh = 0 <= float(age_sec) < lifetime
    LOG.debug('cache age %.1f lifetime %d fresh=%s', age_sec, lifetime, fresh)
    return fresh


__all__ = ['max_age_of', 'is_fresh']
