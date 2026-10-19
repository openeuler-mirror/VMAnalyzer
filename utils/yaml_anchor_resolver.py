"""YAML anchor reference counting.

Over-anchored YAML configs hide sharing that breaks overrides; anchor and
alias counts reveal the sharing density.
"""
import logging
import re

LOG = logging.getLogger(__name__)

ANCHOR_RE = re.compile(r'&([A-Za-z0-9_-]+)')
ALIAS_RE = re.compile(r'\*([A-Za-z0-9_-]+)')


def anchors(text):
    """Return anchor names defined in the YAML text."""
    return ANCHOR_RE.findall(str(text or ''))


def unreferenced_aliases(text):
    """Return alias names without a matching anchor definition."""
    defined = set(anchors(text))
    missing = sorted(a for a in ALIAS_RE.findall(str(text or '')) if a not in defined)
    if missing:
        LOG.warning('dangling yaml aliases %s', missing)
    return missing


__all__ = ['anchors', 'unreferenced_aliases']
