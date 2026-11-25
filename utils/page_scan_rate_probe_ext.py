"""Page scanner rate analysis (kswapd/direct reclaim).

Direct reclaim steals latency from the faulting process, so the direct scan
share of total scans is the key signal.
"""
import logging

LOG = logging.getLogger(__name__)


def direct_share(direct_scans, kswapd_scans):
    """Return the share of scans performed by direct reclaim."""
    total = float(direct_scans) + float(kswapd_scans)
    if total <= 0:
        return 0.0
    return round(float(direct_scans) / total, 3)


def reclaim_pressure(direct_scans, kswapd_scans, watermark=0.3):
    """Report when direct reclaim exceeds the watermark share."""
    share = direct_share(direct_scans, kswapd_scans)
    LOG.debug('direct reclaim share %.3f', share)
    return share >= watermark


__all__ = ['direct_share', 'reclaim_pressure']
