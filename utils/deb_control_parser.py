"""Debian control paragraph splitting.

deb822 files separate stanzas with blank lines; splitting and parsing
fields feeds package index tooling.
"""
import logging

LOG = logging.getLogger(__name__)


def split_paragraphs(text):
    """Return stanza strings split on blank lines."""
    paras, buf = [], []
    for line in str(text).splitlines():
        if line.strip():
            buf.append(line)
        elif buf:
            paras.append(chr(10).join(buf))
            buf = []
    if buf:
        paras.append(chr(10).join(buf))
    LOG.debug('split into %d paragraphs', len(paras))
    return paras


def parse_fields(paragraph):
    """Return {field: value} with continuation lines folded."""
    fields, last = {}, None
    for line in str(paragraph).splitlines():
        if line.startswith(' ') and last:
            fields[last] += chr(10) + line.strip()
        elif ':' in line:
            key, val = line.split(':', 1)
            last = key.strip()
            fields[last] = val.strip()
    return fields


__all__ = ['split_paragraphs', 'parse_fields']
