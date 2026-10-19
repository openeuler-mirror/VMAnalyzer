"""Gzip multi-member counting.

Concatenated gzip files contain several members; counting magic headers
estimates how many streams were appended.
"""
import logging

LOG = logging.getLogger(__name__)
MAGIC = (0x1F, 0x8B)


def member_offsets(data):
    """Return byte offsets where a gzip member header starts."""
    buf = bytes(data)
    offs = []
    for i in range(len(buf) - 1):
        if buf[i] == MAGIC[0] and buf[i + 1] == MAGIC[1]:
            offs.append(i)
    LOG.debug('gzip members at %s', offs[:10])
    return offs


def count_members(data):
    """Return how many gzip members the blob holds."""
    return len(member_offsets(data))


__all__ = ['member_offsets', 'count_members', 'MAGIC']
