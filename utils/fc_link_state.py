"""Fibre Channel link state scoring.

An FC link that flaps between online states corrupts inflight I/O, so state
transitions are scored by instability.
"""
import logging

LOG = logging.getLogger(__name__)


def flap_count(states):
    """Count transitions out of the Online state."""
    seq = [str(s) for s in states or []]
    flaps = 0
    for prev, cur in zip(seq, seq[1:]):
        if prev == 'Online' and cur != 'Online':
            flaps += 1
    return flaps


def stability_score(states):
    """Return 0..1 stability where 1 means never flapped."""
    seq = [str(s) for s in states or []]
    if len(seq) < 2:
        return 1.0
    flaps = flap_count(seq)
    score = max(0.0, 1.0 - flaps / float(len(seq) - 1))
    LOG.debug('fc stability %.3f', score)
    return round(score, 3)


__all__ = ['flap_count', 'stability_score']
