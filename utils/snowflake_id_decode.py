"""Snowflake id decoding.

Twitter-style ids pack millisecond time, worker id and a sequence into
64 bits; splitting the fields aids incident forensics.
"""
import logging

LOG = logging.getLogger(__name__)


def decode(snowflake, epoch_ms=1288834974657):
    """Return {timestamp_ms, worker, sequence} from a snowflake id."""
    value = int(snowflake)
    sequence = value & 0xFFF
    worker = (value >> 12) & 0x3FF
    ts = (value >> 22) + epoch_ms
    LOG.debug('snowflake worker=%d seq=%d', worker, sequence)
    return {'timestamp_ms': ts, 'worker': worker, 'sequence': sequence}


def ids_per_millisecond(snowflakes, epoch_ms=1288834974657):
    """Return the highest sequence seen, a proxy for id burst rate."""
    seqs = [decode(s, epoch_ms)['sequence'] for s in snowflakes or []]
    return max(seqs, default=-1)


__all__ = ['decode', 'ids_per_millisecond']
