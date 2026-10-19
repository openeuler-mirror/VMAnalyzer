"""systemd journal cursor comparison.

Cursors embed a monotonic timestamp; comparing two cursors tells whether a
follower fell behind the writer.
"""
import logging

LOG = logging.getLogger(__name__)


def parse_cursor(cursor):
    """Return the realtime microsecond field of a journal cursor."""
    for part in str(cursor or '').split(';'):
        for kv in part.split(','):
            if kv.startswith('realtime='):
                try:
                    return int(kv.split('=', 1)[1])
                except ValueError:
                    return 0
    return 0


def lag_usec(leader_cursor, follower_cursor):
    """Return how far the follower lags the leader in microseconds."""
    lag = parse_cursor(leader_cursor) - parse_cursor(follower_cursor)
    LOG.debug('journal lag %d us', lag)
    return max(0, lag)


__all__ = ['parse_cursor', 'lag_usec']
