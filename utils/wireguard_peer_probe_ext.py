"""WireGuard peer handshake freshness.

WireGuard is silent without traffic, so the handshake age is the only
liveness signal per peer.
"""
import logging
import time

LOG = logging.getLogger(__name__)


def handshake_age(last_handshake_ts, now=None):
    """Return seconds since the last handshake."""
    moment = time.time() if now is None else float(now)
    return round(max(0.0, moment - float(last_handshake_ts)), 1)


def stale_peers(peers, max_age_sec=180.0, now=None):
    """Return peers whose handshake is older than the threshold."""
    stale = []
    for name, ts in (peers or {}).items():
        if handshake_age(ts, now) > max_age_sec:
            stale.append(name)
    LOG.debug('%d stale wireguard peers', len(stale))
    return sorted(stale)


__all__ = ['handshake_age', 'stale_peers']
