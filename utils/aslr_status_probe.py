"""ASLR randomization audit.

randomize_va_space below two weakens exploit resistance; the value is checked
against the secure default.
"""
import logging

LOG = logging.getLogger(__name__)


def level(value):
    """Return off, conservative or full for the sysctl value."""
    v = int(value if value is not None else -1)
    return {0: 'off', 1: 'conservative', 2: 'full'}.get(v, 'unknown')


def secure(value):
    """Report whether ASLR runs at full strength."""
    ok = level(value) == 'full'
    if not ok:
        LOG.warning('aslr level %s', level(value))
    return ok


__all__ = ['level', 'secure']
