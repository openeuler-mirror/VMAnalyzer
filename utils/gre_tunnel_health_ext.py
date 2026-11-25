"""GRE tunnel keepalive health.

GRE has no native liveness, so missed keepalive replies are counted to decide
when to reroute.
"""
import logging

LOG = logging.getLogger(__name__)


def miss_ratio(sent, received):
    """Return the share of keepalives without a reply."""
    if not sent or sent <= 0:
        return 0.0
    missed = max(0, int(sent) - int(received))
    return round(missed / float(sent), 3)


def should_failover(sent, received, watermark=0.5):
    """Report when the miss ratio justifies failover."""
    ratio = miss_ratio(sent, received)
    LOG.debug('gre keepalive miss %.3f', ratio)
    return ratio >= watermark


__all__ = ['miss_ratio', 'should_failover']
