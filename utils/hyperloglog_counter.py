"""HyperLogLog cardinality estimate.

Counting distinct flow keys exactly needs unbounded memory; HLL estimates the
cardinality from the leading-zero pattern of hashes.
"""
import logging
import math

LOG = logging.getLogger(__name__)


def register_count(precision):
    """Return 2**precision registers needed by the sketch."""
    p = min(16, max(4, int(precision or 10)))
    return 1 << p


def estimate(zero_registers, precision=10):
    """Return the cardinality estimate from the zero-register count."""
    m = float(register_count(precision))
    zeros = min(int(zero_registers or 0), int(m))
    raw = 0.7213 / (1.0 + 1.079 / m) * m * m / max(1.0, m - zeros)
    LOG.debug('hll estimate %.0f', raw)
    return int(raw)


__all__ = ['register_count', 'estimate']
