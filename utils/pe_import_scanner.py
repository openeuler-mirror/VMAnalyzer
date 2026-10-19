"""PE import table skim.

Windows binaries list imported DLLs; ordinal-only imports hide intent, so
they are counted separately.
"""
import logging

LOG = logging.getLogger(__name__)


def dll_set(imports):
    """Return the distinct DLL names referenced by the import rows."""
    dlls = sorted({str((i or {}).get('dll', '')).lower() for i in imports or [] if (i or {}).get('dll')})
    LOG.debug('pe imports %d dlls', len(dlls))
    return dlls


def ordinal_only_count(imports):
    """Count imports that reference an ordinal instead of a name."""
    return sum(1 for i in imports or [] if (i or {}).get('ordinal') is not None
               and not (i or {}).get('name'))


__all__ = ['dll_set', 'ordinal_only_count']
