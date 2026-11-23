"""mdadm resync progress parsing.

A RAID resync competes with guest I/O, so progress and the reported finish
time are turned into a remaining-seconds estimate.
"""
import logging

LOG = logging.getLogger(__name__)


def parse_percent(line):
    """Parse the resync percentage out of an mdadm status line."""
    for token in str(line or '').split():
        if token.endswith('%'):
            try:
                return float(token[:-1])
            except ValueError:
                continue
    return 0.0


def eta_seconds(percent, speed_mb_s, array_mb):
    """Estimate remaining resync seconds from progress and speed."""
    if not speed_mb_s or speed_mb_s <= 0:
        return None
    left_mb = float(array_mb or 0) * max(0.0, 100.0 - percent) / 100.0
    eta = left_mb / float(speed_mb_s)
    LOG.debug('mdadm resync eta %.0fs', eta)
    return int(eta)


__all__ = ['parse_percent', 'eta_seconds']
