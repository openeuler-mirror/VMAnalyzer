"""TCP retransmission analysis.

Retransmissions signal path congestion or receiver overrun and directly degrade
guest throughput even when link utilisation looks low.  These helpers compute
the retransmit share and its trend.
"""
import logging

LOG = logging.getLogger(__name__)


def retransmit_ratio(prev, curr):
    """Return the retransmit share of segments sent over an interval."""
    segments = max(0, int(curr.get('out_segs', 0)) - int(prev.get('out_segs', 0)))
    retrans = max(0, int(curr.get('retrans_segs', 0)) - int(prev.get('retrans_segs', 0)))
    if segments <= 0:
        LOG.debug('no outbound segments in interval')
        return 0.0
    return round(min(1.0, retrans / float(segments)), 6)


def ratio_trend(ratios):
    """Return the direction of a retransmit ratio series."""
    values = [float(r) for r in ratios or [] if r is not None]
    if len(values) < 2:
        return 'flat'
    delta = values[-1] - values[0]
    if delta > 0.005:
        return 'rising'
    if delta < -0.005:
        return 'falling'
    return 'flat'


def worst_socket(sockets):
    """Return the socket with the highest retransmit ratio."""
    if not sockets:
        return None
    return max(sockets, key=lambda s: s.get('ratio', 0.0))


__all__ = ['retransmit_ratio', 'ratio_trend', 'worst_socket']
