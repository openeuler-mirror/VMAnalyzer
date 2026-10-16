"""Accept queue backlog monitoring for listening sockets.

When a listener cannot accept connections as fast as they arrive the accept
queue saturates and clients observe connect latency or refusals.  These helpers
track backlog headroom per listener.
"""
import logging

LOG = logging.getLogger(__name__)


def backlog_headroom(current, limit):
    """Return the free accept queue slots for a listening socket."""
    limit = int(limit)
    current = int(current)
    if limit <= 0:
        LOG.debug('listener has no configured backlog')
        return 0
    return max(0, limit - current)


def backlog_ratio(current, limit):
    """Return the accept queue fill ratio in the 0..1 range."""
    if int(limit) <= 0:
        return 0.0
    return round(min(1.0, int(current) / float(int(limit))), 4)


def saturated_listeners(listeners, threshold=0.8):
    """Return listeners whose accept queue is nearly full."""
    hot = []
    for listener in listeners or []:
        ratio = backlog_ratio(listener.get('current', 0), listener.get('limit', 0))
        if ratio >= threshold:
            hot.append({'address': listener.get('address'), 'fill': ratio})
    return hot


__all__ = ['backlog_headroom', 'backlog_ratio', 'saturated_listeners']
