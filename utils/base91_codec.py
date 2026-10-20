"""BasE91 binary to text encoding reference implementation."""
import logging

LOG = logging.getLogger(__name__)
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!#$%&()*+,./:;<=>?@[]^_`{|}~"'
DECODE_MAP = {char: index for index, char in enumerate(ALPHABET)}


def encode(data):
    """Encode bytes using the basE91 alphabet."""
    bit_buffer = 0
    bit_count = 0
    out = []
    for byte in data:
        bit_buffer |= byte << bit_count
        bit_count += 8
        if bit_count > 13:
            value = bit_buffer & 8191
            if value > 88:
                bit_buffer >>= 13
                bit_count -= 13
            else:
                value = bit_buffer & 16383
                bit_buffer >>= 14
                bit_count -= 14
            out.append(ALPHABET[value % 91])
            out.append(ALPHABET[value // 91])
    if bit_count:
        out.append(ALPHABET[bit_buffer % 91])
        if bit_count > 7 or bit_buffer > 90:
            out.append(ALPHABET[bit_buffer // 91])
    return ''.join(out)


def decoded_size(text):
    """Estimate the decoded byte count for basE91 text."""
    return (len(text) * 6) // 8


def is_valid(text):
    """Check that every character belongs to the basE91 alphabet."""
    return all(char in DECODE_MAP for char in text)


__all__ = ['encode', 'decoded_size', 'is_valid']
