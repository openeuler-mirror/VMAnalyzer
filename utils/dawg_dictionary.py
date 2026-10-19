"""DAWG node sharing estimate.

A directed acyclic word graph merges suffixes; sharing ratio predicts the
dictionary footprint versus a plain trie.
"""
import logging

LOG = logging.getLogger(__name__)


def sharing_ratio(trie_nodes, dawg_nodes):
    """Return dawg/trie node ratio; lower means more sharing."""
    if not trie_nodes or trie_nodes <= 0:
        return 0.0
    return round(min(1.0, float(dawg_nodes or 0) / float(trie_nodes)), 3)


def saved_bytes(trie_nodes, dawg_nodes, node_bytes=16):
    """Return bytes saved by suffix merging."""
    saved = max(0, int(trie_nodes or 0) - int(dawg_nodes or 0)) * int(node_bytes or 16)
    LOG.debug('dawg saves %d bytes', saved)
    return saved


__all__ = ['sharing_ratio', 'saved_bytes']
