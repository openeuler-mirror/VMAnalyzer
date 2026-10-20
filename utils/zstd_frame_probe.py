"""Zstd frame window audit.

Large windows let compressors reference far back but cost decode memory; the
window log is checked against a memory budget.
"""
import logging

LOG = logging.getLogger(__name__)


def window_bytes(window_log):
    """Return the decode window size for the frame window log."""
    wl = max(10, min(31, int(window_log or 22)))
    return 1 << wl


def fits_budget(window_log, budget_mb):
    """Report whether the window fits the decode memory budget."""
    fits = window_bytes(window_log) <= int(budget_mb or 0) * (1 << 20)
    LOG.debug('zstd window log %s fits=%s', window_log, fits)
    return fits


__all__ = ['window_bytes', 'fits_budget']
