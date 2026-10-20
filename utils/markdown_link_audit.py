"""Markdown dangling link audit.

Docs rot when relative links point at renamed files; link targets are listed
so a checker can verify each exists.
"""
import logging
import re

LOG = logging.getLogger(__name__)

LINK_RE = re.compile(r'\[[^\]]*\]\(([^)]+)\)')


def link_targets(text):
    """Return all link targets found in the markdown text."""
    return LINK_RE.findall(str(text or ''))


def relative_targets(text):
    """Return link targets that are neither absolute URLs nor anchors."""
    rel = [t for t in link_targets(text)
           if not t.startswith(('http://', 'https://', '#', 'mailto:'))]
    LOG.debug('md relative links %d', len(rel))
    return rel


__all__ = ['link_targets', 'relative_targets']
