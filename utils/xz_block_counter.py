"""XZ block size estimate.

XZ streams split into independent blocks; the block count bounds parallel
decompression threads.
"""
import logging

LOG = logging.getLogger(__name__)


def threads_for_blocks(block_count, max_threads=8):
    """Return how many decompression threads are worth spawning."""
    t = max(1, min(int(max_threads or 1), int(block_count or 1)))
    LOG.debug('xz threads %d', t)
    return t


def block_memory(dict_size, threads):
    """Return the memory needed for parallel xz decompression."""
    return int(dict_size or 0) * int(threads or 1) * 3


__all__ = ['threads_for_blocks', 'block_memory']
