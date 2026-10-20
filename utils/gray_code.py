"""Gray code encoding, decoding and sequence generation."""
import logging

LOG = logging.getLogger(__name__)


def encode(value):
    """Return the Gray code of a non-negative integer."""
    number = int(value)
    if number < 0:
        raise ValueError('value must be non-negative')
    return number ^ (number >> 1)


def decode(code):
    """Return the binary integer represented by a Gray code."""
    number = int(code)
    if number < 0:
        raise ValueError('code must be non-negative')
    result = number
    while number:
        number >>= 1
        result ^= number
    return result


def sequence(bits):
    """Return the full reflected Gray code sequence of the given bit width."""
    width = int(bits)
    if width < 0:
        raise ValueError('bits must be non-negative')
    return [encode(index) for index in range(1 << width)]


__all__ = ['encode', 'decode', 'sequence']
