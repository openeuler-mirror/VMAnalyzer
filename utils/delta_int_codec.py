"""Delta encoding of monotonic and signed integer sequences."""
import logging

LOG = logging.getLogger(__name__)


def encode_deltas(values):
    """Encode a sequence as its first value plus successive deltas."""
    encoded = []
    previous = 0
    for value in values:
        encoded.append(value - previous)
        previous = value
    return encoded


def decode_deltas(deltas, start=0):
    """Rebuild the original sequence from a delta stream."""
    result = []
    current = start
    for delta in deltas:
        current += delta
        result.append(current)
    return result


def max_delta(values):
    """Return the largest absolute delta in a sequence."""
    if len(values) < 2:
        return 0
    return max(abs(delta) for delta in encode_deltas(values)[1:])


__all__ = ['encode_deltas', 'decode_deltas', 'max_delta']
