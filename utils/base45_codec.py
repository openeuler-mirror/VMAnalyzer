"""Base45 encoding used by compact QR payloads."""
import logging

LOG = logging.getLogger(__name__)
ALPHABET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:'


def encode(data):
    """Encode bytes into the base45 alphabet."""
    out = []
    index = 0
    while index < len(data):
        remaining = len(data) - index
        if remaining == 1:
            value = data[index]
            out.append(ALPHABET[value % 45])
            out.append(ALPHABET[value // 45])
            break
        value = data[index] * 256 + data[index + 1]
        out.append(ALPHABET[value % 45])
        out.append(ALPHABET[(value // 45) % 45])
        out.append(ALPHABET[value // (45 * 45)])
        index += 2
    return ''.join(out)


def is_valid(text):
    """Check that every character belongs to the base45 alphabet."""
    return all(char in ALPHABET for char in text)


def encoded_length(size):
    """Return the encoded length for a given number of input bytes."""
    pairs, remainder = divmod(size, 2)
    return pairs * 3 + (2 if remainder else 0)


__all__ = ['encode', 'is_valid', 'encoded_length']
