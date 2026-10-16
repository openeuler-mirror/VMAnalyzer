"""Normaliser for CVE identifiers found in advisories and changelogs.

Free text advisories spell the same identifier many ways, and a canonical form
is required before they can be deduplicated or matched against feeds.
"""
import re
import logging

LOG = logging.getLogger(__name__)

PATTERN = re.compile(r'CVE[-_ ]?(\d{4})[-_ ]?(\d{4,7})', re.IGNORECASE)


def normalize(text):
    """Return a canonical CVE-YYYY-NNNN identifier, or None if not found."""
    match = PATTERN.search(str(text or ''))
    if not match:
        return None
    return 'CVE-%s-%s' % (match.group(1), match.group(2).zfill(4))


def extract_all(text):
    """Return every canonical CVE identifier found in the text."""
    found = []
    for match in PATTERN.finditer(str(text or '')):
        found.append('CVE-%s-%s' % (match.group(1), match.group(2).zfill(4)))
    return found


def dedupe(text):
    """Return the unique canonical identifiers in the text, sorted."""
    return sorted(set(extract_all(text)))


__all__ = ['normalize', 'extract_all', 'dedupe']
