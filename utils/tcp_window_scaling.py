"""TCP window scale negotiation audit.

A missing window scale option caps throughput on high BDP paths, so the
advertised scale factors are validated against the link profile.
"""
import logging

LOG = logging.getLogger(__name__)

MAX_SCALE = 14


def effective_window(window, scale):
    """Return the real window size after applying the scale factor."""
    return int(window) << max(0, min(MAX_SCALE, int(scale)))


def scale_for_bandwidth(bandwidth_bps, rtt_sec):
    """Return the smallest scale factor covering the bandwidth delay product."""
    bdp = float(bandwidth_bps) * float(rtt_sec) / 8.0
    scale = 0
    while (65535 << scale) < bdp and scale < MAX_SCALE:
        scale += 1
    LOG.debug('bdp %.0f needs scale %d', bdp, scale)
    return scale


__all__ = ['effective_window', 'scale_for_bandwidth']
