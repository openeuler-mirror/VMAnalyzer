"""Mach-O load command census.

Load commands describe dylibs and rpaths; a census spots unexpected dynamic
dependencies in shipped binaries.
"""
import logging
from collections import Counter

LOG = logging.getLogger(__name__)


def command_counts(commands):
    """Return {command name: count} for the load command list."""
    counts = Counter(str(c or '').upper() for c in commands or [])
    LOG.debug('mach-o commands %s', dict(counts))
    return dict(counts)


def rpath_entries(commands_detail):
    """Return the rpath strings embedded in the binary."""
    return [str((c or {}).get('path'))
            for c in commands_detail or []
            if str((c or {}).get('cmd', '')).upper() == 'LC_RPATH']


__all__ = ['command_counts', 'rpath_entries']
