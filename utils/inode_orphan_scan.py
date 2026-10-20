"""Orphaned inode accounting.

Inodes without directory entries hold space hostage after crashes, so orphan
counts per filesystem are ranked for cleanup.
"""
import logging

LOG = logging.getLogger(__name__)


def worst_fs(orphan_counts):
    """Return the filesystem with the most orphaned inodes."""
    best, best_n = None, -1
    for fs, count in (orphan_counts or {}).items():
        if int(count or 0) > best_n:
            best, best_n = fs, int(count or 0)
    LOG.debug('worst orphan fs %s count=%d', best, best_n)
    return best


def cleanup_worthwhile(orphan_counts, floor=100):
    """Return filesystems whose orphan count justifies a fsck run."""
    return sorted(fs for fs, c in (orphan_counts or {}).items() if int(c or 0) >= floor)


__all__ = ['worst_fs', 'cleanup_worthwhile']
