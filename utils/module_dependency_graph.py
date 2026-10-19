"""Kernel module dependency depth.

Deep modprobe chains slow boot; depth per module derives from the depends
edges.
"""
import logging

LOG = logging.getLogger(__name__)


def depth_of(module, depends, _memo=None):
    """Return the dependency depth of one module."""
    memo = _memo if _memo is not None else {}
    if module in memo:
        return memo[module]
    deps = (depends or {}).get(module, [])
    memo[module] = 1 + max((depth_of(d, depends, memo) for d in deps), default=0)
    return memo[module]


def deepest(depends):
    """Return the module with the deepest dependency chain."""
    best, best_d = None, -1
    for m in (depends or {}):
        d = depth_of(m, depends)
        if d > best_d:
            best, best_d = m, d
    LOG.debug('deepest module %s depth %d', best, best_d)
    return best


__all__ = ['depth_of', 'deepest']
