"""NFS client retransmit ratio.

Retransmitted RPC calls mean the server or the network drops requests, so
retransmits are set against the total call count.
"""
import logging

LOG = logging.getLogger(__name__)


def retrans_ratio(calls, retrans):
    """Return retransmits per call in 0..1."""
    if not calls or calls <= 0:
        return 0.0
    return round(min(1.0, float(retrans or 0) / float(calls)), 4)


def verdict(ratio, ceiling=0.02):
    """Classify the mount as healthy or strained."""
    verdict = 'strained' if ratio >= ceiling else 'healthy'
    LOG.debug('nfs retrans %.4f -> %s', ratio, verdict)
    return verdict


__all__ = ['retrans_ratio', 'verdict']
