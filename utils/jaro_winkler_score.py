"""Jaro-Winkler prefix boost.

Name matching boosts strings sharing a prefix; the boost scales with prefix
length up to four characters.
"""
import logging

LOG = logging.getLogger(__name__)


def prefix_boost(prefix_len, scale=0.1):
    """Return the Winkler boost for the shared prefix length."""
    return min(4, int(prefix_len or 0)) * float(scale or 0.1)


def apply_boost(jaro, prefix_len, scale=0.1):
    """Return the boosted similarity, capped at one."""
    score = float(jaro or 0) + (1.0 - float(jaro or 0)) * prefix_boost(prefix_len, scale)
    LOG.debug('jaro %.3f boosted %.3f', jaro or 0, score)
    return round(min(1.0, score), 4)


__all__ = ['prefix_boost', 'apply_boost']
