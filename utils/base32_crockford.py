"""Crockford base32 alphabet encoding and decoding."""
import logging

LOG = logging.getLogger(__name__)
ALPHABET = '0123456789ABCDEFGHJKMNPQRSTVWXYZ'
DECODE_MAP = {char: index for index, char in enumerate(ALPHABET)}


def encode(number, length=0):
    """Encode a non negative integer using Crockford base32."""
    if number < 0:
        raise ValueError('number must be non negative')
    if number == 0:
        text = ALPHABET[0]
    else:
        digits = []
        while number:
            number, rem = divmod(number, 32)
            digits.append(ALPHABET[rem])
        text = ''.join(reversed(digits))
    return text.rjust(length, ALPHABET[0])


def decode(text):
    """Decode Crockford base32 text into an integer."""
    value = 0
    for char in text.upper().replace('-', ''):
        if char not in DECODE_MAP:
            raise ValueError('invalid Crockford base32 character: ' + char)
        value = value * 32 + DECODE_MAP[char]
    return value


__all__ = ['encode', 'decode']
