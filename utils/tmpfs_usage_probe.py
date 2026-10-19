"""tmpfs usage accounting.

tmpfs pages live in memory, so a full tmpfs doubles as memory pressure; usage
is reported together with the memory-share equivalent.
"""
import logging

LOG = logging.getLogger(__name__)


def usage_ratio(used_bytes, size_bytes):
    """Return used/size for the tmpfs in 0..1."""
    if not size_bytes or size_bytes <= 0:
        return 0.0
    return round(min(1.0, float(used_bytes or 0) / float(size_bytes)), 4)


def memory_share(used_bytes, total_mem_bytes):
    """Return the share of RAM currently pinned by this tmpfs."""
    if not total_mem_bytes or total_mem_bytes <= 0:
        return 0.0
    share = float(used_bytes or 0) / float(total_mem_bytes)
    LOG.debug('tmpfs pins %.2f%% of RAM', share * 100.0)
    return round(share, 4)


__all__ = ['usage_ratio', 'memory_share']
