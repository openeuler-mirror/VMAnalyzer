"""TLS handshake latency decomposition.

Splitting handshake time into tcp and tls phases shows whether the network or
the crypto stack owns the latency.
"""
import logging

LOG = logging.getLogger(__name__)


def tls_share(tcp_ms, total_ms):
    """Return the share of total time spent after TCP connect."""
    if not total_ms or total_ms <= 0:
        return 0.0
    share = (float(total_ms) - float(tcp_ms)) / float(total_ms)
    return round(max(0.0, min(1.0, share)), 3)


def classify(tcp_ms, total_ms, watermark=0.6):
    """Classify the bottleneck as network or crypto."""
    share = tls_share(tcp_ms, total_ms)
    LOG.debug('tls share %.3f', share)
    return 'crypto' if share >= watermark else 'network'


__all__ = ['tls_share', 'classify']
