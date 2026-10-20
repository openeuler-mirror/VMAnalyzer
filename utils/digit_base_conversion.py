"""Conversion of integers between arbitrary positional bases."""
import logging

LOG = logging.getLogger(__name__)

DIGITS = '0123456789abcdefghijklmnopqrstuvwxyz'


def to_base(value, base):
    """Return the string representation of value in the given base."""
    radix = int(base)
    if not 2 <= radix <= len(DIGITS):
        raise ValueError('base out of the supported range')
    number = int(value)
    if number == 0:
        return '0'
    sign = '-' if number < 0 else ''
    number = abs(number)
    out = []
    while number:
        number, remainder = divmod(number, radix)
        out.append(DIGITS[remainder])
    return sign + ''.join(reversed(out))


def from_base(text, base):
    """Return the integer value of text interpreted in the given base."""
    radix = int(base)
    if not 2 <= radix <= len(DIGITS):
        raise ValueError('base out of the supported range')
    cleaned = str(text).strip().lower()
    sign = 1
    if cleaned.startswith('-'):
        sign = -1
        cleaned = cleaned[1:]
    result = 0
    for char in cleaned:
        result = result * radix + DIGITS.index(char)
    return sign * result


def rebase(text, source_base, target_base):
    """Return text converted from one base to another."""
    return to_base(from_base(text, source_base), target_base)


__all__ = ['to_base', 'from_base', 'rebase']
