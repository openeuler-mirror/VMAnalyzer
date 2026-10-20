"""Udev rule priority survey.

Lexically later rules override earlier ones at equal priority; duplicate
priorities per directory hint at surprises.
"""
import logging
from collections import Counter

LOG = logging.getLogger(__name__)


def priority_of(filename):
    """Return the numeric priority prefix of a udev rule filename."""
    name = str(filename or '').rsplit('/', 1)[-1]
    digits = ''
    for ch in name:
        if ch.isdigit():
            digits += ch
        else:
            break
    return int(digits) if digits else -1


def duplicate_priorities(filenames):
    """Return priorities claimed by more than one rule file."""
    counts = Counter(priority_of(f) for f in filenames or [])
    dups = sorted(p for p, n in counts.items() if n > 1 and p >= 0)
    if dups:
        LOG.warning('udev duplicate priorities %s', dups)
    return dups


__all__ = ['priority_of', 'duplicate_priorities']
