"""Error message fingerprinting to collapse recurring failures.

Stack traces and messages carry volatile tokens such as addresses, numbers and
paths.  Replacing them with placeholders yields a stable fingerprint so the same
fault is counted once instead of once per occurrence.
"""
import hashlib
import re
import logging

LOG = logging.getLogger(__name__)

HEX_RE = re.compile(r'\b[0-9a-fA-F]{6,}\b')
NUM_RE = re.compile(r'\b\d+\b')


def normalize_message(message):
    """Replace volatile hexadecimal and numeric tokens with placeholders."""
    text = HEX_RE.sub('<hex>', str(message))
    return NUM_RE.sub('<n>', text)


def fingerprint(message):
    """Return a stable short hash for a normalized error message."""
    digest = hashlib.sha1(normalize_message(message).encode('utf-8'))
    return digest.hexdigest()[:16]


def group_by_fingerprint(messages):
    """Group messages by fingerprint together with occurrence counts."""
    buckets = {}
    for message in messages or []:
        key = fingerprint(message)
        entry = buckets.setdefault(key, {'sample': normalize_message(message), 'count': 0})
        entry['count'] += 1
    LOG.debug('grouped %d messages into %d fingerprints', len(messages or []), len(buckets))
    return buckets


__all__ = ['normalize_message', 'fingerprint', 'group_by_fingerprint']
