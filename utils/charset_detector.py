"""Charset heuristic scorer.

Legacy logs arrive as latin-1 or cp1252; a byte-frequency score picks the
most plausible single-byte charset.
"""
import logging

LOG = logging.getLogger(__name__)

CP1252_ONLY = set(range(0x80, 0xA0)) - {0x81, 0x8D, 0x8F, 0x90, 0x9D}


def cp1252_score(data):
    """Return the share of high bytes that only exist in cp1252."""
    blob = bytes(data or b'')
    high = [b for b in blob if b >= 0x80]
    if not high:
        return 0.0
    score = sum(1 for b in high if b in CP1252_ONLY) / float(len(high))
    LOG.debug('cp1252 score %.3f', score)
    return round(score, 3)


def guess(data):
    """Return the guessed charset name for the bytes."""
    blob = bytes(data or b'')
    try:
        blob.decode('utf-8')
        return 'utf-8'
    except UnicodeDecodeError:
        return 'cp1252' if cp1252_score(blob) > 0.3 else 'latin-1'


__all__ = ['cp1252_score', 'guess']
