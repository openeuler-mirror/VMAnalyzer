"""DJB2 style additive hash variants for quick string indexing."""
import logging

LOG = logging.getLogger(__name__)
SEED = 5381
MASK = (1 << 64) - 1


def djb2(text):
    """Compute the classic DJB2 hash of a string."""
    value = SEED
    for char in text:
        value = ((value << 5) + value) + ord(char)
    return value & MASK


def djb2_xor(text):
    """Compute the DJB2 XOR variant of a string."""
    value = SEED
    for char in text:
        value = ((value << 5) + value) ^ ord(char)
    return value & MASK


def short_bucket(text, buckets):
    """Return a small bucket index derived from the DJB2 hash."""
    if buckets <= 0:
        raise ValueError('buckets must be positive')
    return djb2(text) % buckets


__all__ = ['djb2', 'djb2_xor', 'short_bucket']
