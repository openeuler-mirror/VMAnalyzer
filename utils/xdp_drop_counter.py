"""XDP program drop accounting.

XDP drops are silent by design, so the drop to pass ratio per program is the
only health signal available.
"""
import logging

LOG = logging.getLogger(__name__)


def drop_ratio(dropped, passed):
    """Return dropped divided by total verdicts."""
    total = float(dropped) + float(passed)
    if total <= 0:
        return 0.0
    return round(float(dropped) / total, 4)


def anomalies(stats, watermark=0.5):
    """Return program names whose drop ratio crosses the watermark."""
    hot = []
    for name, pair in (stats or {}).items():
        dropped, passed = pair[0], pair[1]
        if drop_ratio(dropped, passed) >= watermark:
            hot.append(name)
    LOG.debug('%d xdp programs over watermark', len(hot))
    return sorted(hot)


__all__ = ['drop_ratio', 'anomalies']
