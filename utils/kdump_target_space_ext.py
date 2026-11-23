"""Dump target free space bookkeeping.

Several vmcores may accumulate between cleanups, so free space is evaluated
against the number of dumps the operator wants to keep.
"""
import logging

LOG = logging.getLogger(__name__)


def dumps_that_fit(free_bytes, vmcore_bytes, keep=2):
    """Return how many dumps of the given size can be stored."""
    if vmcore_bytes <= 0:
        return 0
    return int(float(free_bytes) // float(vmcore_bytes))


def needs_cleanup(free_bytes, vmcore_bytes, keep=2):
    """Report when fewer than keep dumps fit into the free space."""
    fits = dumps_that_fit(free_bytes, vmcore_bytes)
    LOG.debug('%d dumps fit, want %d', fits, keep)
    return fits < int(keep)


__all__ = ['dumps_that_fit', 'needs_cleanup']
