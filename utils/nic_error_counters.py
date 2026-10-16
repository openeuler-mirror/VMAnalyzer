"""NIC hardware error counter interpretation.

Physical and virtual NICs expose counters for framing, carrier and rx length
errors.  Unlike drops these are not congestion related and usually point at a
bad link, so they are reported separately.
"""
import logging

LOG = logging.getLogger(__name__)

HARD_ERROR_KEYS = ('rx_crc_errors', 'rx_frame_errors', 'rx_length_errors',
                   'rx_over_errors', 'tx_carrier_errors')


def delta_counters(prev, curr):
    """Return the per counter delta between two snapshots."""
    delta = {}
    for key in HARD_ERROR_KEYS:
        before = int(prev.get(key, 0))
        after = int(curr.get(key, 0))
        delta[key] = max(0, after - before)
    return delta


def total_hard_errors(delta):
    """Sum all hardware error deltas into a single count."""
    return sum(int(v) for v in (delta or {}).values())


def link_verdict(delta, tolerance=0):
    """Judge the link as clean or suspect from hardware error deltas."""
    total = total_hard_errors(delta)
    if total > tolerance:
        LOG.info('link reported %d hardware errors', total)
        return 'suspect'
    return 'clean'


__all__ = ['delta_counters', 'total_hard_errors', 'link_verdict']
