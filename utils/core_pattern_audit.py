"""core_pattern configuration audit.

A core_pattern pointing at a full or missing directory loses crash dumps, so
the pattern is validated for writability constraints.
"""
import logging
import os

LOG = logging.getLogger(__name__)


def is_piped(pattern):
    """Report whether the pattern pipes cores into a helper program."""
    return str(pattern or '').strip().startswith('|')


def target_dir(pattern):
    """Return the directory part of a file based core pattern."""
    if is_piped(pattern):
        return ''
    return os.path.dirname(str(pattern or '').strip())


def audit(pattern):
    """Return a dict describing the pattern configuration."""
    piped = is_piped(pattern)
    directory = target_dir(pattern)
    LOG.debug('core_pattern piped=%s dir=%s', piped, directory)
    return {'piped': piped, 'dir': directory,
            'needs_dir_check': not piped and bool(directory)}


__all__ = ['is_piped', 'target_dir', 'audit']
