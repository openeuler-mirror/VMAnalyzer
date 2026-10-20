"""Aho-Corasick automaton sizing.

Multi-pattern log scanning builds goto/failure tables; state count grows with
the summed pattern length.
"""
import logging

LOG = logging.getLogger(__name__)


def state_count(patterns):
    """Return the worst-case automaton state count."""
    states = 1 + sum(len(str(p)) for p in patterns or [])
    LOG.debug('aho-corasick states %d', states)
    return states


def memory_bytes(patterns, edge_size=8, alphabet=256):
    """Return a dense goto-table footprint estimate."""
    return state_count(patterns) * int(alphabet or 256) * int(edge_size or 8)


__all__ = ['state_count', 'memory_bytes']
