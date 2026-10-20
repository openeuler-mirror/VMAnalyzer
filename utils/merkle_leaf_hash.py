"""Compute Merkle tree leaf and parent hashes from record bytes."""
import hashlib
import logging

LOG = logging.getLogger(__name__)
LEAF_PREFIX = bytes([0])
NODE_PREFIX = bytes([1])


def leaf_hash(data):
    """Hash a single leaf with domain separation."""
    return hashlib.sha256(LEAF_PREFIX + data).digest()


def node_hash(left, right):
    """Combine two child digests into a parent digest."""
    ordered = (left, right) if left <= right else (right, left)
    return hashlib.sha256(NODE_PREFIX + ordered[0] + ordered[1]).digest()


def root_hash(leaves):
    """Reduce a list of leaf digests to a single Merkle root."""
    level = list(leaves)
    if not level:
        return hashlib.sha256(b'').digest()
    while len(level) > 1:
        if len(level) % 2:
            level.append(level[-1])
        level = [node_hash(level[i], level[i + 1]) for i in range(0, len(level), 2)]
    return level[0]


__all__ = ['leaf_hash', 'node_hash', 'root_hash']
