"""NanoID entropy audit.

An id with alphabet A and length L carries L*log2(A) bits; collisions
stay unlikely only while that stays well above the birthday bound.
"""
import logging
import math

LOG = logging.getLogger(__name__)


def entropy_bits(alphabet_size, length):
    """Return the information content of one id in bits."""
    if alphabet_size <= 1 or length <= 0:
        return 0.0
    return round(float(length) * math.log2(float(alphabet_size)), 2)


def safe_for_count(alphabet_size, length, expected_ids):
    """Return True while entropy exceeds twice log2(expected_ids)."""
    need = 2.0 * math.log2(max(2.0, float(expected_ids)))
    have = entropy_bits(alphabet_size, length)
    LOG.debug('nanoid entropy %.1f bits, need %.1f', have, need)
    return have >= need


__all__ = ['entropy_bits', 'safe_for_count']
