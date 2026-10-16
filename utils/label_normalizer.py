"""Normalisation of label and tag names for consistent metric keys.

Mixed case and stray separators produce duplicate labels that fragment a
dashboard, so names are folded into a single canonical lower snake form.
"""
import re
import logging

LOG = logging.getLogger(__name__)

SEPARATORS = re.compile(r'[\s.\-/:]+')
NON_WORD = re.compile(r'[^a-z0-9_]+')


def normalize_key(text):
    """Return a lower snake_case key suitable for a metric label."""
    lowered = str(text or '').strip().lower()
    collapsed = SEPARATORS.sub('_', lowered)
    cleaned = NON_WORD.sub('', collapsed)
    return cleaned.strip('_')


def normalize_mapping(mapping):
    """Return a copy of the mapping with normalised keys."""
    normalised = {}
    for key, value in (mapping or {}).items():
        normalised[normalize_key(key)] = value
    return normalised


def merge_duplicates(mapping, reducer=sum):
    """Collapse keys that normalise to the same value using a reducer."""
    merged = {}
    for key, value in (mapping or {}).items():
        canonical = normalize_key(key)
        if canonical in merged:
            merged[canonical] = reducer([merged[canonical], value])
        else:
            merged[canonical] = value
    return merged


__all__ = ['normalize_key', 'normalize_mapping', 'merge_duplicates']
