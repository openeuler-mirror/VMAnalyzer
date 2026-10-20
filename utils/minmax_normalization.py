"""Min-max scaling and range normalisation for numeric series."""
import logging

LOG = logging.getLogger(__name__)


def min_max(values):
    """Return the (minimum, maximum) pair, or (0.0, 0.0) when empty."""
    items = [float(v) for v in values or []]
    if not items:
        return 0.0, 0.0
    return min(items), max(items)


def normalize(values, low=0.0, high=1.0):
    """Return values rescaled into the low..high interval."""
    items = [float(v) for v in values or []]
    if not items:
        return []
    minimum, maximum = min(items), max(items)
    if maximum == minimum:
        return [(low + high) / 2.0 for _ in items]
    span = high - low
    return [low + (v - minimum) / (maximum - minimum) * span for v in items]


def denormalize(values, minimum, maximum, low=0.0, high=1.0):
    """Return scaled values mapped back to the original numeric range."""
    if high == low:
        raise ValueError('low and high must differ')
    span = high - low
    return [minimum + (float(v) - low) / span * (maximum - minimum)
            for v in values or []]


__all__ = ['min_max', 'normalize', 'denormalize']
