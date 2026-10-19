"""ELF section entropy estimate.

Packed or encrypted sections show byte entropy near eight bits; a coarse
histogram flags suspicious sections without external tools.
"""
import logging
import math
from collections import Counter

LOG = logging.getLogger(__name__)


def byte_entropy(data):
    """Return Shannon entropy in bits per byte of the data."""
    blob = bytes(data or b'')
    if not blob:
        return 0.0
    counts = Counter(blob)
    n = float(len(blob))
    ent = -sum(c / n * math.log(c / n, 2) for c in counts.values())
    return round(ent, 3)


def suspicious(entropy, ceiling=7.2):
    """Report when entropy suggests packing or encryption."""
    sus = float(entropy or 0) >= ceiling
    LOG.debug('section entropy %.3f suspicious=%s', entropy, sus)
    return sus


__all__ = ['byte_entropy', 'suspicious']
