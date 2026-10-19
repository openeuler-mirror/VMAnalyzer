"""TIME_WAIT socket accounting.

Huge TIME_WAIT counts consume slots without carrying data; the rate of new
TIME_WAITs per second is the actionable number.
"""
import logging

LOG = logging.getLogger(__name__)


def share_of_total(tw_count, total_sockets):
    """Return the TIME_WAIT share of all sockets."""
    if not total_sockets or total_sockets <= 0:
        return 0.0
    return round(max(0.0, min(1.0, float(tw_count) / float(total_sockets))), 3)


def needs_recycle(tw_count, total_sockets, watermark=0.4):
    """Report when TIME_WAIT sockets dominate the table."""
    share = share_of_total(tw_count, total_sockets)
    LOG.debug('timewait share %.3f', share)
    return share >= watermark


__all__ = ['share_of_total', 'needs_recycle']
