"""Polynomial string hashing with a configurable modulus."""
import logging

LOG = logging.getLogger(__name__)
DEFAULT_BASE = 131
DEFAULT_MOD = 1000000007


def poly_hash(text, base=DEFAULT_BASE, modulus=DEFAULT_MOD):
    """Hash a string into an integer using a polynomial scheme."""
    value = 0
    for char in text:
        value = (value * base + ord(char)) % modulus
    return value


def prefix_hashes(text, base=DEFAULT_BASE, modulus=DEFAULT_MOD):
    """Return every prefix hash value for a string."""
    value = 0
    result = []
    for char in text:
        value = (value * base + ord(char)) % modulus
        result.append(value)
    return result


def collides(left, right, base=DEFAULT_BASE, modulus=DEFAULT_MOD):
    """Report whether two strings share the same polynomial hash."""
    return poly_hash(left, base, modulus) == poly_hash(right, base, modulus)


__all__ = ['poly_hash', 'prefix_hashes', 'collides']
