"""Read only file system detection.

A file system remounts read only after an IO error to protect data, which
silently breaks writers until an operator intervenes.
"""
import logging

LOG = logging.getLogger(__name__)

READ_ONLY_FLAGS = ('ro', 'readonly', 'read-only')


def is_read_only(mount_options):
    """Report whether the option list marks a mount read only."""
    options = str(mount_options).lower().replace(' ', '')
    return any(flag in options.split(',') for flag in READ_ONLY_FLAGS)


def find_read_only(mounts):
    """Return the mounts that are currently read only."""
    flagged = [m.get('path') for m in mounts or [] if is_read_only(m.get('options', ''))]
    if flagged:
        LOG.warning('%d mounts are read only', len(flagged))
    return flagged


def write_verdict(mounts, expected_writable):
    """Judge whether a mount that should be writable is read only."""
    blocked = [path for path in find_read_only(mounts) if path in (expected_writable or [])]
    return 'blocked' if blocked else 'ok'


__all__ = ['is_read_only', 'find_read_only', 'write_verdict']
