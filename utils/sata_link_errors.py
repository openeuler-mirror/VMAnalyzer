"""SATA link error counter delta.

CRC and handshake errors on a SATA link usually mean a failing cable, so
deltas between polls are classified by severity.
"""
import logging

LOG = logging.getLogger(__name__)


def error_delta(prev, cur):
    """Return the per-counter delta between two snapshots."""
    out = {}
    for key, val in (cur or {}).items():
        out[key] = max(0, int(val or 0) - int((prev or {}).get(key, 0)))
    return out


def severity(delta):
    """Classify a delta snapshot as clean, noisy or failing."""
    total = sum((delta or {}).values())
    if total == 0:
        return 'clean'
    if total < 10:
        return 'noisy'
    LOG.warning('sata link failing delta=%s', delta)
    return 'failing'


__all__ = ['error_delta', 'severity']
