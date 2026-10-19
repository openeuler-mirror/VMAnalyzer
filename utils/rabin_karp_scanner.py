"""Rabin-Karp rolling hash modulus.

Rolling hashes collide by birthday bound; the modulus is chosen so collisions
stay rare for the expected window count.
"""
import logging

LOG = logging.getLogger(__name__)


def modulus_for_windows(window_count):
    """Return a prime-ish modulus keeping collisions below one percent."""
    n = max(1, int(window_count or 1))
    mod = 1
    target = n * n * 100
    while mod < target:
        mod = mod * 2 + 1
    LOG.debug('rabin-karp modulus %d', mod)
    return mod


def collision_risk(window_count, modulus):
    """Return the approximate collision probability."""
    if not modulus or modulus <= 0:
        return 1.0
    n = float(window_count or 0)
    return round(min(1.0, n * n / (2.0 * float(modulus))), 6)


__all__ = ['modulus_for_windows', 'collision_risk']
