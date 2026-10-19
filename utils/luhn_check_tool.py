"""Luhn checksum.

Card numbers and many ids carry a Luhn digit; validating it catches
transcription errors before a payment round-trip.
"""
import logging

LOG = logging.getLogger(__name__)


def luhn_valid(digits):
    """Return True when the digit string passes Luhn."""
    nums = [int(c) for c in str(digits) if c.isdigit()]
    if not nums:
        return False
    total = 0
    for i, d in enumerate(reversed(nums)):
        if i % 2 == 1:
            d = d * 2 - 9 if d * 2 > 9 else d * 2
        total += d
    return total % 10 == 0


def check_digit(prefix):
    """Return the digit that makes prefix Luhn-valid."""
    for cand in '0123456789':
        if luhn_valid(str(prefix) + cand):
            LOG.debug('luhn check digit %s', cand)
            return cand
    return None


__all__ = ['luhn_valid', 'check_digit']
