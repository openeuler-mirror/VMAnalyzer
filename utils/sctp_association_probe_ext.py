"""SCTP association path audit.

Multi homed SCTP associations are only as strong as their weakest path, so
per path state is aggregated into an association health flag.
"""
import logging

LOG = logging.getLogger(__name__)


def active_paths(path_states):
    """Return the count of paths in ACTIVE state."""
    return sum(1 for s in path_states or [] if str(s).upper() == 'ACTIVE')


def degraded(path_states):
    """Report when at least one path is down but the association lives."""
    states = [str(s).upper() for s in path_states or []]
    if not states:
        return False
    alive = sum(1 for s in states if s == 'ACTIVE')
    LOG.debug('sctp paths %d/%d active', alive, len(states))
    return 0 < alive < len(states)


__all__ = ['active_paths', 'degraded']
