"""TOML dotted section collision check.

Merging two TOML files fails when both define the same table; section headers
are compared before writing the merged file.
"""
import logging
import re

LOG = logging.getLogger(__name__)

SECTION_RE = re.compile(r'^\s*\[+\s*([^\]]+?)\s*\]+')


def sections(text):
    """Return the normalised section names of a TOML document."""
    out = []
    for line in str(text or '').splitlines():
        m = SECTION_RE.match(line)
        if m:
            out.append(m.group(1).replace(' ', ''))
    return out


def collisions(text_a, text_b):
    """Return sections defined by both documents."""
    both = sorted(set(sections(text_a)) & set(sections(text_b)))
    if both:
        LOG.warning('toml section collisions %s', both)
    return both


__all__ = ['sections', 'collisions']
