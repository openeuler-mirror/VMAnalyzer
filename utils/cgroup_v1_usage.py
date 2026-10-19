"""cgroup v1 memory usage parsing.

Usage under the limit still triggers reclaim when cache dominates; the
rss-vs-cache split is derived from the stat rows.
"""
import logging

LOG = logging.getLogger(__name__)


def rss_share(stat_rows):
    """Return rss/(rss+cache) from cgroup v1 memory.stat rows."""
    rows = {str(k): float(v) for k, v in (stat_rows or {}).items()}
    rss = rows.get('rss', 0.0)
    cache = rows.get('cache', 0.0)
    total = rss + cache
    return round(rss / total, 3) if total else 0.0


def near_limit(usage_bytes, limit_bytes, margin=0.9):
    """Report when usage crossed the margin of the limit."""
    if not limit_bytes or limit_bytes <= 0:
        return False
    near = float(usage_bytes or 0) >= margin * float(limit_bytes)
    LOG.debug('cgroup v1 near limit=%s', near)
    return near


__all__ = ['rss_share', 'near_limit']
