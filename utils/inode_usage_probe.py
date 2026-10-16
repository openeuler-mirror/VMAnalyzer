"""Inode exhaustion detection for guest file systems.

A file system can report plenty of free space yet refuse to create files once
its inode table is exhausted.  These helpers track inode pressure separately
from block usage.
"""
import logging

LOG = logging.getLogger(__name__)


def inode_usage(used, total):
    """Return the inode usage ratio for a file system."""
    total = int(total)
    used = int(used)
    if total <= 0:
        LOG.debug('file system reports zero inode capacity')
        return 0.0
    return round(min(1.0, used / float(total)), 4)


def risky_mounts(mounts, threshold=0.9):
    """Return mounts whose inode usage reaches the alert threshold."""
    risky = []
    for mount in mounts or []:
        ratio = inode_usage(mount.get('inodes_used', 0), mount.get('inodes_total', 0))
        if ratio >= threshold:
            risky.append({'mount': mount.get('path'), 'inode_ratio': ratio})
    return risky


def headroom_inodes(used, total):
    """Return how many inodes can still be allocated."""
    return max(0, int(total) - int(used))


__all__ = ['inode_usage', 'risky_mounts', 'headroom_inodes']
