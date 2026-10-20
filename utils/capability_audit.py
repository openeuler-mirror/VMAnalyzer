"""Linux capability bounding set audit.

Daemons should drop unused capabilities; the effective set is diffed against
the documented need.
"""
import logging

LOG = logging.getLogger(__name__)


def unexpected(effective, documented):
    """Return effective capabilities that are not documented."""
    extra = sorted(set(str(c) for c in effective or []) - set(str(c) for c in documented or []))
    if extra:
        LOG.warning('unexpected caps %s', extra)
    return extra


def missing(effective, documented):
    """Return documented capabilities that are not effective."""
    return sorted(set(str(c) for c in documented or []) - set(str(c) for c in effective or []))


__all__ = ['unexpected', 'missing']
