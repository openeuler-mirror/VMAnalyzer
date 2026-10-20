"""Base62 short identifier encoding for compact URLs."""
import logging

LOG = logging.getLogger(__name__)
ALPHABET = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


def encode(value, length=0, alphabet=ALPHABET):
    """Encode a non negative integer into base62 text."""
    if value < 0:
        raise ValueError('value must be non negative')
    base = len(alphabet)
    if value == 0:
        text = alphabet[0]
    else:
        digits = []
        while value:
            value, rem = divmod(value, base)
            digits.append(alphabet[rem])
        text = ''.join(reversed(digits))
    return text.rjust(length, alphabet[0])


def decode(text, alphabet=ALPHABET):
    """Decode base62 text back into an integer."""
    base = len(alphabet)
    lookup = {char: index for index, char in enumerate(alphabet)}
    value = 0
    for char in text:
        value = value * base + lookup[char]
    return value


__all__ = ['encode', 'decode']
