"""Packet loss estimation from interface counters.

Loss is derived from the growth of receive errors and drops relative to the
total frames seen, which distinguishes congestion drops from corrupt frames.
"""
import logging

LOG = logging.getLogger(__name__)


def loss_rate(prev, curr):
    """Return drop and error rates over an interval between two snapshots."""
    frames = max(0, int(curr.get('rx_frames', 0)) - int(prev.get('rx_frames', 0)))
    drops = max(0, int(curr.get('rx_drops', 0)) - int(prev.get('rx_drops', 0)))
    errors = max(0, int(curr.get('rx_errors', 0)) - int(prev.get('rx_errors', 0)))
    if frames <= 0:
        LOG.debug('no frames received in interval')
        return {'drop_rate': 0.0, 'error_rate': 0.0}
    return {
        'drop_rate': round(drops / float(frames), 6),
        'error_rate': round(errors / float(frames), 6),
    }


def is_lossy(rates, drop_limit=0.001, error_limit=0.0005):
    """Report whether drop or error rates exceed tolerated limits."""
    return rates.get('drop_rate', 0) > drop_limit or rates.get('error_rate', 0) > error_limit


def loss_severity(rates, drop_limit=0.001):
    """Grade the loss as none, low or high relative to a limit."""
    rate = max(rates.get('drop_rate', 0.0), rates.get('error_rate', 0.0))
    if rate <= 0:
        return 'none'
    if rate >= drop_limit * 10:
        return 'high'
    return 'low'


__all__ = ['loss_rate', 'is_lossy', 'loss_severity']
