"""Block device service time histogram utilities.

Service time is bucketed by the kernel into fixed latency slots.  Reconstructing
a coarse cumulative distribution lets a checker flag tail latency without
needing every individual request.
"""
import logging

LOG = logging.getLogger(__name__)

DEFAULT_BUCKETS_MS = (1, 2, 4, 8, 16, 32, 64, 128)


def bucketize(samples, buckets=DEFAULT_BUCKETS_MS):
    """Count samples into half open latency buckets."""
    counts = [0] * (len(buckets) + 1)
    for sample in samples or []:
        value = float(sample)
        placed = False
        for index, upper in enumerate(buckets):
            if value < upper:
                counts[index] += 1
                placed = True
                break
        if not placed:
            counts[-1] += 1
    return counts


def cumulative_share(counts):
    """Return the cumulative share of each bucket over all samples."""
    total = sum(counts)
    if total == 0:
        LOG.debug('empty histogram')
        return [0.0] * len(counts)
    running = 0
    shares = []
    for count in counts:
        running += count
        shares.append(round(running / float(total), 4))
    return shares


def tail_share(counts, buckets=DEFAULT_BUCKETS_MS, threshold_ms=64):
    """Return the share of samples slower than threshold_ms."""
    total = sum(counts)
    if total == 0:
        return 0.0
    index = len(buckets)
    for i, upper in enumerate(buckets):
        if threshold_ms <= upper:
            index = i
            break
    return round(sum(counts[index:]) / float(total), 4)


__all__ = ['bucketize', 'cumulative_share', 'tail_share']
