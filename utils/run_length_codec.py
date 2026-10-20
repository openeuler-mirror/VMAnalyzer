"""Run length encoding for sequences of hashable items."""
import logging

LOG = logging.getLogger(__name__)


def encode(items):
    """Encode a sequence as (item, run_length) pairs."""
    encoded = []
    for item in items:
        if encoded and encoded[-1][0] == item:
            encoded[-1][1] += 1
        else:
            encoded.append([item, 1])
    return [tuple(pair) for pair in encoded]


def decode(pairs):
    """Expand (item, run_length) pairs back into a flat list."""
    result = []
    for item, count in pairs:
        if count < 0:
            raise ValueError('run length must not be negative')
        result.extend([item] * count)
    return result


def compression_ratio(items, pairs):
    """Return the encoded to original length ratio."""
    if not items:
        return 1.0
    return round(len(pairs) / float(len(items)), 4)


__all__ = ['encode', 'decode', 'compression_ratio']
