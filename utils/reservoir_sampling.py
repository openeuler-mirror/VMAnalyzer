"""Uniform reservoir sampling over an unseen length stream."""
import logging
import random

LOG = logging.getLogger(__name__)


def reservoir_sample(iterable, size, rng=None):
    """Return a uniform random sample of the given size from the stream."""
    if size <= 0:
        raise ValueError('size must be positive')
    generator = rng or random
    reservoir = []
    for index, item in enumerate(iterable or []):
        if index < size:
            reservoir.append(item)
        else:
            swap = generator.randrange(index + 1)
            if swap < size:
                reservoir[swap] = item
    return reservoir


def weighted_reservoir_sample(entries, size, rng=None):
    """Return a sample biased by the weight attached to each entry."""
    generator = rng or random
    reservoir = []
    for key, weight in entries or []:
        score = generator.random() ** (1.0 / float(weight)) if weight else 0.0
        reservoir.append((score, key))
    reservoir.sort(reverse=True)
    return [key for _, key in reservoir[:size]]


def sample_fraction(iterable, fraction, rng=None):
    """Return each element with probability equal to fraction."""
    generator = rng or random
    return [item for item in iterable or [] if generator.random() < fraction]


__all__ = ['reservoir_sample', 'weighted_reservoir_sample', 'sample_fraction']
