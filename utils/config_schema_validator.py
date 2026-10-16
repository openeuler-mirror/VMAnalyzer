"""Lightweight schema validation for agent configuration documents.

Instead of pulling in a full validation library the agent checks required keys,
expected types and numeric ranges directly and returns human readable problems.
"""
import logging

LOG = logging.getLogger(__name__)


def validate_required(document, required_keys):
    """Return the configuration keys that are missing."""
    missing = [key for key in required_keys if key not in (document or {})]
    if missing:
        LOG.info('configuration missing keys: %s', ', '.join(missing))
    return missing


def validate_types(document, expected):
    """Return type mismatches as (key, expected, actual) triples."""
    problems = []
    for key, kind in (expected or {}).items():
        if key in document and not isinstance(document[key], kind):
            problems.append((key, kind.__name__, type(document[key]).__name__))
    return problems


def validate_ranges(document, ranges):
    """Return keys whose numeric value falls outside an allowed range."""
    outside = []
    for key, (low, high) in (ranges or {}).items():
        value = document.get(key)
        if isinstance(value, (int, float)) and not low <= value <= high:
            outside.append((key, value))
    return outside


__all__ = ['validate_required', 'validate_types', 'validate_ranges']
