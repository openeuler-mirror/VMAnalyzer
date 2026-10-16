"""Time based log de-duplication.

Identical messages repeated in a tight loop should be collapsed to a single
emission plus a repeat counter, otherwise one noisy service can flood the
collection pipeline.
"""
import logging

LOG = logging.getLogger(__name__)


def dedup(messages):
    """Collapse consecutive duplicate messages while counting repeats."""
    result = []
    for message in messages or []:
        if result and result[-1]['message'] == message:
            result[-1]['repeat'] += 1
        else:
            result.append({'message': message, 'repeat': 1})
    LOG.debug('deduplicated %d messages into %d groups', len(messages or []), len(result))
    return result


def dampened_stream(messages, repeat_limit=3):
    """Return only runs short enough to still be interesting."""
    return [entry for entry in dedup(messages) if entry['repeat'] <= repeat_limit]


def repeat_stats(deduped):
    """Return the maximum and total repeat counts of a deduplicated stream."""
    repeats = [entry.get('repeat', 1) for entry in deduped or []]
    return {'max_repeat': max(repeats, default=0), 'total': sum(repeats)}


__all__ = ['dedup', 'dampened_stream', 'repeat_stats']
