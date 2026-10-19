"""UTF-8 continuation byte audit.

Mojibake in logs comes from invalid continuation bytes; counting them per
line locates the corrupt source.
"""
import logging

LOG = logging.getLogger(__name__)


def invalid_continuations(data):
    """Return the count of stray continuation bytes in the data."""
    blob = bytes(data or b'')
    bad = 0
    i = 0
    while i < len(blob):
        b = blob[i]
        if b < 0x80:
            i += 1
        elif b < 0xC0:
            bad += 1
            i += 1
        elif b < 0xE0:
            i += 2
        elif b < 0xF0:
            i += 3
        else:
            i += 4
    LOG.debug('utf8 stray continuations %d', bad)
    return bad


def clean_ratio(data):
    """Return the share of lines that decode cleanly."""
    lines = bytes(data or b'').splitlines() or [b'']
    ok = 0
    for line in lines:
        try:
            line.decode('utf-8')
            ok += 1
        except UnicodeDecodeError:
            pass
    return round(ok / float(len(lines)), 3)


__all__ = ['invalid_continuations', 'clean_ratio']
