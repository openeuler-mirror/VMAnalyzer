"""Modular arithmetic helpers using binary exponentiation."""
import logging

LOG = logging.getLogger(__name__)


def pow_mod(base, exponent, modulus):
    """Return base raised to exponent modulo modulus in logarithmic time."""
    if modulus <= 0:
        raise ValueError('modulus must be positive')
    power = int(exponent)
    if power < 0:
        raise ValueError('exponent must be non-negative')
    result = 1
    current = int(base) % modulus
    while power:
        if power & 1:
            result = result * current % modulus
        current = current * current % modulus
        power >>= 1
    return result


def mod_inverse(value, modulus):
    """Return the multiplicative inverse of value modulo modulus."""
    old_r, r = int(value) % modulus, modulus
    old_s, s = 1, 0
    while r:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
    if old_r != 1:
        raise ValueError('value is not invertible modulo modulus')
    return old_s % modulus


def mod_pow_series(bases, exponents, modulus):
    """Return modular powers for paired bases and exponents."""
    return [pow_mod(b, e, modulus)
            for b, e in zip(bases or [], exponents or [])]


__all__ = ['pow_mod', 'mod_inverse', 'mod_pow_series']
