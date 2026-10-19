"""Markdown heading outline.

Long runbooks need a table of contents; headings are collected with their
levels and slugified anchors.
"""
import logging
import re

LOG = logging.getLogger(__name__)

HEADING_RE = re.compile(r'^(#{1,6})\s+(.*)$')


def outline(text):
    """Return (level, title) pairs for every ATX heading."""
    out = []
    for line in str(text or '').splitlines():
        m = HEADING_RE.match(line)
        if m:
            out.append((len(m.group(1)), m.group(2).strip()))
    LOG.debug('md headings %d', len(out))
    return out


def slug(title):
    """Return the GitHub-style anchor slug for a heading."""
    s = re.sub(r'[^a-z0-9 -]', '', str(title or '').lower())
    return s.replace(' ', '-')


__all__ = ['outline', 'slug']
