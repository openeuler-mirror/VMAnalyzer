"""Crash kernel reservation parsing.

The crashkernel= boot parameter syntax is easy to get wrong across kernel
versions, so it is parsed into a canonical range form.
"""
import logging
import re

LOG = logging.getLogger(__name__)

PATTERN = re.compile(r'^(\d+[MmGg])(?:-(\d+[MmGg]))?(?::(\d+[MmGg]))?$')
UNITS = {'M': 1 << 20, 'G': 1 << 30}


def to_bytes(text):
    """Convert a size string like 256M or 2G into bytes."""
    match = re.match(r'^(\d+)([MmGg])$', str(text or '').strip())
    if not match:
        return 0
    return int(match.group(1)) * UNITS[match.group(2).upper()]


def parse(value):
    """Parse a crashkernel value into {'size': bytes, 'offset': bytes}."""
    match = PATTERN.match(str(value or '').strip())
    if not match:
        LOG.debug('unparseable crashkernel %s', value)
        return None
    return {'size': to_bytes(match.group(1)), 'offset': to_bytes(match.group(3) or '0M')}


__all__ = ['to_bytes', 'parse']
