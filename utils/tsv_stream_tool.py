"""TSV row width guard.

Tabs inside free-text fields shift every column; rows whose field count
differs from the header are quarantined.
"""
import logging

LOG = logging.getLogger(__name__)


def bad_rows(lines, header_fields):
    """Return zero-based indexes of rows with a wrong field count."""
    bad = []
    for i, line in enumerate(lines or []):
        if len(str(line).split('	')) != int(header_fields or 0):
            bad.append(i)
    if bad:
        LOG.warning('tsv bad rows %s', bad[:5])
    return bad


def field_count(line):
    """Return the tab-separated field count of one row."""
    return len(str(line or '').split('	'))


__all__ = ['bad_rows', 'field_count']
