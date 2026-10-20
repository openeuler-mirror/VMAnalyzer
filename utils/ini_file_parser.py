"""INI duplicate key detection.

Last-one-wins parsers silently drop earlier values; duplicates per section
are surfaced before the file is rewritten.
"""
import logging

LOG = logging.getLogger(__name__)


def duplicates(text):
    """Return {(section, key): occurrence count} for repeated keys."""
    from collections import Counter
    seen = Counter()
    section = ''
    for line in str(text or '').splitlines():
        s = line.strip()
        if s.startswith('[') and s.endswith(']'):
            section = s[1:-1].strip()
        elif '=' in s and not s.startswith(('#', ';')):
            key = s.split('=', 1)[0].strip()
            seen[(section, key)] += 1
    dups = {k: v for k, v in seen.items() if v > 1}
    if dups:
        LOG.warning('ini duplicates %s', list(dups)[:5])
    return dups


def section_names(text):
    """Return section names in document order."""
    return [l.strip()[1:-1].strip() for l in str(text or '').splitlines()
            if l.strip().startswith('[') and l.strip().endswith(']')]


__all__ = ['duplicates', 'section_names']
