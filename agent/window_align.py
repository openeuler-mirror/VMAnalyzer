"""Align metric aggregation windows across collectors.

Collectors with different intervals still need to agree on window
boundaries.  A shared alignment helper prevents partial windows at the start
of each report.
"""

import logging

LOG = logging.getLogger(__name__)


def align_start(timestamp, window, epoch=0):
    """Return the start of the aligned window containing a timestamp."""
    if window <= 0:
        raise ValueError("window must be positive")
    offset = (float(timestamp) - epoch) % window
    return float(timestamp) - offset


def align_end(timestamp, window, epoch=0):
    """Return the exclusive end of the aligned window."""
    return align_start(timestamp, window, epoch) + window


def align_range(start, end, window, epoch=0):
    """Expand a range outward to full window boundaries."""
    if float(end) <= float(start):
        return float(start), float(start)
    aligned_start = align_start(start, window, epoch)
    aligned_end = align_end(max(float(start), float(end) - 1e-9), window, epoch)
    LOG.debug("aligned range %.3f..%.3f into %.3f..%.3f",
              start, end, aligned_start, aligned_end)
    return aligned_start, aligned_end
