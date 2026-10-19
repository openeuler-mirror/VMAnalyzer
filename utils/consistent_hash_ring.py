"""Consistent hash ring balance.

Virtual nodes smooth key distribution; the coefficient of variation of vnode
loads measures how even the ring is.
"""
import logging

LOG = logging.getLogger(__name__)


def load_cv(vnode_loads):
    """Return the coefficient of variation of vnode loads."""
    vals = [float(v) for v in vnode_loads or [] if v is not None]
    if not vals:
        return 0.0
    mean = sum(vals) / len(vals)
    if mean <= 0:
        return 0.0
    var = sum((v - mean) ** 2 for v in vals) / len(vals)
    cv = (var ** 0.5) / mean
    LOG.debug('ring load cv %.3f', cv)
    return round(cv, 3)


def vnodes_for_cv(nodes, target_cv=0.1):
    """Return suggested vnodes per physical node for the target cv."""
    return max(10, int((1.0 / max(0.01, target_cv)) ** 2 / max(1, nodes) * 10))


__all__ = ['load_cv', 'vnodes_for_cv']
