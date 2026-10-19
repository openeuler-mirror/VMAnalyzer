"""Streaming JSON value counter.

Large exports arrive as concatenated JSON values; counting them without
loading the whole file keeps memory flat.
"""
import json
import logging

LOG = logging.getLogger(__name__)


def iter_values(text):
    """Yield decoded JSON values from concatenated text."""
    decoder = json.JSONDecoder()
    idx, end = 0, len(text)
    while idx < end:
        while idx < end and text[idx].isspace():
            idx += 1
        if idx >= end:
            break
        try:
            value, idx = decoder.raw_decode(text, idx)
        except ValueError:
            LOG.debug('stopping at byte %d', idx)
            break
        yield value


def count_values(text):
    """Return how many JSON values the stream contains."""
    return sum(1 for _ in iter_values(text))


__all__ = ['iter_values', 'count_values']
