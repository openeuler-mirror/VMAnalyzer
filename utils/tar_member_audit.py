"""Tar member path safety.

Archive extraction must reject absolute paths and parent traversal;
auditing names before untar stops zip-slip style escapes.
"""
import logging

LOG = logging.getLogger(__name__)


def unsafe_names(member_names):
    """Return member names that escape the extraction root."""
    bad = []
    for name in member_names or []:
        n = str(name)
        if n.startswith('/') or n.startswith('~'):
            bad.append(n)
            continue
        parts = [p for p in n.split('/') if p not in ('', '.')]
        if '..' in parts:
            bad.append(n)
    LOG.debug('unsafe tar members %d', len(bad))
    return bad


def has_pax_headers(member_names):
    """Return True when any member looks like a pax extended header."""
    return any(str(n).endswith('PaxHeader') or str(n).startswith('./PaxHeaders')
               for n in member_names or [])


__all__ = ['unsafe_names', 'has_pax_headers']
