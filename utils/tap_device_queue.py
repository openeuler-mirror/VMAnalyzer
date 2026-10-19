"""TAP device transmit queue audit.

A persistently full tx queue on a tap device drops guest packets silently, so
queue lengths are scored against their configured size.
"""
import logging

LOG = logging.getLogger(__name__)


def fill_ratio(qlen, txqueuelen):
    """Return 0..1 fill of the transmit queue."""
    if not txqueuelen or txqueuelen <= 0:
        return 0.0
    return round(max(0.0, min(1.0, float(qlen) / float(txqueuelen))), 3)


def congested(devices, watermark=0.8):
    """Return names of tap devices above the fill watermark."""
    hot = []
    for name, pair in (devices or {}).items():
        qlen, size = pair[0], pair[1]
        if fill_ratio(qlen, size) >= watermark:
            hot.append(name)
    LOG.debug('%d congested tap devices', len(hot))
    return sorted(hot)


__all__ = ['fill_ratio', 'congested']
