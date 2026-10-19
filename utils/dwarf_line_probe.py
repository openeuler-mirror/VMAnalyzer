"""DWARF line table coverage.

Stripped or partial debug info shows up as addresses without line mapping;
coverage is the mapped share of code bytes.
"""
import logging

LOG = logging.getLogger(__name__)


def line_coverage(mapped_bytes, total_code_bytes):
    """Return the share of code bytes that carry line info."""
    if not total_code_bytes or total_code_bytes <= 0:
        return 0.0
    return round(min(1.0, float(mapped_bytes or 0) / float(total_code_bytes)), 3)


def sparse_regions(address_rows, gap_threshold=4096):
    """Count gaps in the line table larger than the threshold."""
    rows = sorted(int(a) for a in address_rows or [] if a is not None)
    gaps = sum(1 for a, b in zip(rows, rows[1:]) if b - a > gap_threshold)
    LOG.debug('dwarf sparse gaps %d', gaps)
    return gaps


__all__ = ['line_coverage', 'sparse_regions']
