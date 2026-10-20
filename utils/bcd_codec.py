"""Binary coded decimal packing for fixed width numeric fields."""
import logging

LOG = logging.getLogger(__name__)
DIGITS = '0123456789'


def encode_digits(text):
    """Pack an even length digit string into BCD bytes."""
    if any(char not in DIGITS for char in text):
        raise ValueError('only decimal digits are allowed')
    if len(text) % 2:
        text = '0' + text
    packed = bytearray()
    for index in range(0, len(text), 2):
        packed.append((int(text[index]) << 4) | int(text[index + 1]))
    return bytes(packed)


def decode_digits(data):
    """Unpack BCD bytes back into a digit string."""
    digits = []
    for byte in data:
        high = byte >> 4
        low = byte & 0x0F
        if high > 9 or low > 9:
            raise ValueError('invalid BCD nibble')
        digits.append(str(high))
        digits.append(str(low))
    return ''.join(digits)


def as_integer(data):
    """Return the integer value represented by BCD bytes."""
    return int(decode_digits(data) or '0')


__all__ = ['encode_digits', 'decode_digits', 'as_integer']
