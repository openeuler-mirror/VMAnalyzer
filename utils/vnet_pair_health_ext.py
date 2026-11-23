"""veth pair link state check.

Both ends of a veth pair must agree on link state; a half down pair silently
drops traffic between guest and host.
"""
import logging

LOG = logging.getLogger(__name__)

UP = 'UP'


def is_pair_up(host_state, peer_state):
    """Report whether both ends report UP."""
    return str(host_state).upper() == UP and str(peer_state).upper() == UP


def broken_pairs(pairs):
    """Return names of pairs whose ends disagree or are down."""
    broken = []
    for name, states in (pairs or {}).items():
        host, peer = states[0], states[1]
        if not is_pair_up(host, peer):
            broken.append(name)
    LOG.debug('%d broken veth pairs', len(broken))
    return sorted(broken)


__all__ = ['is_pair_up', 'broken_pairs']
