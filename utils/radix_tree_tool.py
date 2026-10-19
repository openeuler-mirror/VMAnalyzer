"""Radix tree compression estimate.

Compressing unary chains shrinks routing tables; the ratio of compressed
nodes to raw nodes predicts memory saved.
"""
import logging

LOG = logging.getLogger(__name__)


def compression_ratio(raw_nodes, compressed_nodes):
    """Return compressed/raw node ratio in 0..1."""
    if not raw_nodes or raw_nodes <= 0:
        return 0.0
    return round(min(1.0, float(compressed_nodes or 0) / float(raw_nodes)), 3)


def saved_nodes(raw_nodes, compressed_nodes):
    """Return the node count eliminated by compression."""
    saved = max(0, int(raw_nodes or 0) - int(compressed_nodes or 0))
    LOG.debug('radix saved %d nodes', saved)
    return saved


__all__ = ['compression_ratio', 'saved_nodes']
