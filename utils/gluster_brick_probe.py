"""Gluster brick online audit.

Replicated volumes silently lose redundancy when one brick goes offline;
grouping brick state by volume finds the exposed volumes.
"""
import logging

LOG = logging.getLogger(__name__)


def offline_by_volume(bricks):
    """Return {volume: [offline brick paths]}."""
    offline = {}
    for brick in bricks or []:
        if not brick.get('online', False):
            offline.setdefault(brick.get('volume', 'unknown'), []).append(
                brick.get('path', '?'))
    LOG.debug('volumes with offline bricks: %d', len(offline))
    return offline


def volume_redundant(bricks, volume, min_online=2):
    """Return True when the volume keeps at least min_online bricks."""
    online = sum(1 for b in bricks or []
                 if b.get('volume') == volume and b.get('online', False))
    return online >= min_online


__all__ = ['offline_by_volume', 'volume_redundant']
