"""Structural diff between two configuration dictionaries.

Comparing a desired with an observed configuration shows exactly which keys were
added, removed or changed, which is the basis of configuration drift detection.
"""
import logging

LOG = logging.getLogger(__name__)


def diff_dicts(before, after, path=''):
    """Return added, removed and changed leaf values between two mappings."""
    added = {}
    removed = {}
    changed = {}
    for key in set(before or {}) | set(after or {}):
        full = '%s.%s' % (path, key) if path else str(key)
        if key not in before:
            added[full] = after[key]
        elif key not in after:
            removed[full] = before[key]
        elif isinstance(before[key], dict) and isinstance(after[key], dict):
            sub = diff_dicts(before[key], after[key], full)
            added.update(sub['added'])
            removed.update(sub['removed'])
            changed.update(sub['changed'])
        elif before[key] != after[key]:
            changed[full] = {'from': before[key], 'to': after[key]}
    return {'added': added, 'removed': removed, 'changed': changed}


def has_drift(diff):
    """Report whether any addition, removal or change was detected."""
    return bool(diff.get('added') or diff.get('removed') or diff.get('changed'))


def drift_size(diff):
    """Return the total number of differing keys."""
    return (len(diff.get('added', {})) + len(diff.get('removed', {}))
            + len(diff.get('changed', {})))


__all__ = ['diff_dicts', 'has_drift', 'drift_size']
