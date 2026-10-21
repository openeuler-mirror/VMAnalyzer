"""Shorten UUID strings into compact base62 identifiers."""
import logging
import uuid

LOG = logging.getLogger(__name__)
ALPHABET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'


def encode_int(value, alphabet=ALPHABET):
    """Encode a non negative integer into a custom alphabet."""
    if value < 0:
        raise ValueError('value must be non negative')
    base = len(alphabet)
    if value == 0:
        return alphabet[0]
    digits = []
    while value:
        value, rem = divmod(value, base)
        digits.append(alphabet[rem])
    return ''.join(reversed(digits))


def shorten(value, alphabet=ALPHABET):
    """Compress a UUID into a shorter base62 representation."""
    if isinstance(value, str):
        value = uuid.UUID(value)
    return encode_int(value.int, alphabet)


def expand(text, alphabet=ALPHABET):
    """Rebuild a UUID object from a shortened base62 string."""
    base = len(alphabet)
    lookup = {char: index for index, char in enumerate(alphabet)}
    value = 0
    for char in text:
        value = value * base + lookup[char]
    return uuid.UUID(int=value)


__all__ = ['encode_int', 'shorten', 'expand']
