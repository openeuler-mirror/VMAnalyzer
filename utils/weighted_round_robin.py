"""Weighted round robin sequence.

Smooth WRR avoids bursts to high-weight backends; the current-weight table is
advanced one pick at a time.
"""
import logging

LOG = logging.getLogger(__name__)


def next_pick(current, weights):
    """Advance the smooth WRR state and return the picked backend name."""
    total = sum(int(w or 0) for w in (weights or {}).values())
    best = None
    for name, w in (weights or {}).items():
        current[name] = int(current.get(name, 0)) + int(w or 0)
        if best is None or current[name] > current[best]:
            best = name
    if best is not None:
        current[best] -= total
    LOG.debug('wrr picked %s', best)
    return best


def normalise_weights(weights):
    """Return weights divided by their GCD for compact state."""
    from math import gcd
    vals = [int(w or 0) for w in (weights or {}).values() if w]
    g = 0
    for v in vals:
        g = gcd(g, v)
    if g <= 1:
        return dict(weights or {})
    return {k: int(v or 0) // g for k, v in (weights or {}).items()}


__all__ = ['next_pick', 'normalise_weights']
