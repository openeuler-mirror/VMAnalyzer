"""ELF symbol binding census.

Undefined weak symbols resolve at runtime and break static analysis, so
bindings are tallied per object.
"""
import logging
from collections import Counter

LOG = logging.getLogger(__name__)


def binding_counts(symbols):
    """Return {binding: count} for the symbol rows."""
    counts = Counter(str((s or {}).get('bind', 'LOCAL')).upper() for s in symbols or [])
    LOG.debug('elf bindings %s', dict(counts))
    return dict(counts)


def undefined_weaks(symbols):
    """Return names of weak symbols with no definition."""
    return sorted(str((s or {}).get('name'))
                  for s in symbols or []
                  if str((s or {}).get('bind', '')).upper() == 'WEAK'
                  and not (s or {}).get('defined'))


__all__ = ['binding_counts', 'undefined_weaks']
