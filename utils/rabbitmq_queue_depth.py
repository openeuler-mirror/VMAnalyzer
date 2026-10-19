"""RabbitMQ queue depth triage.

Ready messages show consumer starvation while unacked messages point at
slow or stuck consumers; the split matters for paging decisions.
"""
import logging

LOG = logging.getLogger(__name__)


def classify_queue(ready, unacked, ready_warn=1000, unacked_warn=500):
    """Return ok/starving/stuck/busy for one queue."""
    if ready >= ready_warn and unacked < unacked_warn:
        state = 'starving'
    elif unacked >= unacked_warn:
        state = 'stuck'
    elif ready >= ready_warn:
        state = 'busy'
    else:
        state = 'ok'
    LOG.debug('queue ready=%d unacked=%d -> %s', ready, unacked, state)
    return state


def worst_queues(queue_rows, limit=5):
    """Return queues sorted by ready depth descending."""
    rows = sorted(queue_rows or [], key=lambda r: r.get('ready', 0), reverse=True)
    return rows[:limit]


__all__ = ['classify_queue', 'worst_queues']
