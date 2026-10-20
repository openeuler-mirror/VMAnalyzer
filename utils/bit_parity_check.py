"""Even parity and XOR checksum helpers for integer payloads."""
import logging

LOG = logging.getLogger(__name__)


def is_even_parity(value):
    """Return whether the number of set bits in value is even."""
    return bin(int(value)).count('1') % 2 == 0


def parity_bit(value):
    """Return the bit that makes the payload's set bit count even."""
    return bin(int(value)).count('1') % 2


def add_parity(value, width):
    """Return value with an even parity bit placed above the given width."""
    return int(value) | (parity_bit(value) << int(width))


def xor_checksum(values):
    """Return the running XOR of every value as a compact checksum."""
    result = 0
    for value in values or []:
        result ^= int(value)
    return result


__all__ = ['is_even_parity', 'parity_bit', 'add_parity', 'xor_checksum']
