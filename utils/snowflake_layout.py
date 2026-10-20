"""Snowflake style identifier layout with worker and sequence bits."""
import logging
import time

LOG = logging.getLogger(__name__)
EPOCH_MS = 1288834974657
WORKER_BITS = 10
SEQUENCE_BITS = 12
MAX_WORKER = (1 << WORKER_BITS) - 1
MAX_SEQUENCE = (1 << SEQUENCE_BITS) - 1


def compose(timestamp_ms, worker, sequence):
    """Assemble an identifier from its component fields."""
    if not 0 <= worker <= MAX_WORKER:
        raise ValueError('worker out of range')
    if not 0 <= sequence <= MAX_SEQUENCE:
        raise ValueError('sequence out of range')
    delta = timestamp_ms - EPOCH_MS
    return (delta << (WORKER_BITS + SEQUENCE_BITS)) | (worker << SEQUENCE_BITS) | sequence


def decompose(identifier):
    """Split an identifier back into timestamp, worker and sequence."""
    sequence = identifier & MAX_SEQUENCE
    worker = (identifier >> SEQUENCE_BITS) & MAX_WORKER
    timestamp = (identifier >> (WORKER_BITS + SEQUENCE_BITS)) + EPOCH_MS
    return {'timestamp_ms': timestamp, 'worker': worker, 'sequence': sequence}


def now_ms():
    """Return the current wall clock in milliseconds."""
    return int(time.time() * 1000)


__all__ = ['compose', 'decompose', 'now_ms']
