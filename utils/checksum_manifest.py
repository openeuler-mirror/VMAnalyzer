"""Compare expected and observed checksums for a set of files."""
import logging

LOG = logging.getLogger(__name__)


def parse_manifest(text):
    """Parse lines of checksum and path into an ordered mapping."""
    entries = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = line.split(None, 1)
        if len(parts) != 2:
            raise ValueError('malformed manifest line: ' + line)
        entries[parts[1].strip()] = parts[0].strip().lower()
    return entries


def diff(expected, observed):
    """Return missing, extra and mismatched entries between two mappings."""
    missing = sorted(set(expected) - set(observed))
    extra = sorted(set(observed) - set(expected))
    changed = sorted(path for path in set(expected) & set(observed)
                     if expected[path] != observed[path])
    return {'missing': missing, 'extra': extra, 'mismatched': changed}


def is_clean(result):
    """Report whether a diff contains no drift at all."""
    return not (result['missing'] or result['extra'] or result['mismatched'])


__all__ = ['parse_manifest', 'diff', 'is_clean']
