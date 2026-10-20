"""Seccomp filter strictness.

Filters logging instead of blocking syscall abuse give false comfort; the
default action decides the strictness tier.
"""
import logging

LOG = logging.getLogger(__name__)

TIERS = {'SCMP_ACT_KILL': 3, 'SCMP_ACT_KILL_PROCESS': 3, 'SCMP_ACT_ERRNO': 2,
         'SCMP_ACT_LOG': 1, 'SCMP_ACT_ALLOW': 0}


def tier(default_action):
    """Return the strictness tier of the filter default action."""
    t = TIERS.get(str(default_action or '').upper(), -1)
    LOG.debug('seccomp %s -> tier %d', default_action, t)
    return t


def enforces(default_action):
    """Report whether the default action actually blocks."""
    return tier(default_action) >= 2


__all__ = ['tier', 'enforces']
