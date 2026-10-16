"""Recursive merge of layered configuration overrides.

Operator overrides are layered on top of defaults, and a deep merge preserves
untouched nested keys instead of replacing whole sections.
"""
import logging

LOG = logging.getLogger(__name__)


def deep_merge(base, override):
    """Return a new mapping where override wins over base, recursively."""
    result = dict(base or {})
    for key, value in (override or {}).items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    LOG.debug('merged override carrying %d top level keys', len(override or {}))
    return result


def merge_all(layers):
    """Merge a sequence of layers from lowest to highest precedence."""
    result = {}
    for layer in layers or []:
        result = deep_merge(result, layer)
    return result


def conflicts(base, override):
    """Return the top level keys present in both layers."""
    return sorted(set(base or {}) & set(override or {}))


__all__ = ['deep_merge', 'merge_all', 'conflicts']
