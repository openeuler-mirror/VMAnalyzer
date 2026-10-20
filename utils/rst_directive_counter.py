"""reStructuredText directive census.

Sphinx directives like .. note:: and .. warning:: cluster in risky runbooks;
counts per directive guide style review.
"""
import logging
import re
from collections import Counter

LOG = logging.getLogger(__name__)

DIRECTIVE_RE = re.compile(r'^\.\.\s+([a-z0-9_-]+)::', re.IGNORECASE | re.MULTILINE)


def directive_counts(text):
    """Return {directive: count} for the document."""
    counts = Counter(m.lower() for m in DIRECTIVE_RE.findall(str(text or '')))
    LOG.debug('rst directives %d kinds', len(counts))
    return dict(counts)


def has_toctree(text):
    """Report whether the document embeds a toctree."""
    return 'toctree' in directive_counts(text)


__all__ = ['directive_counts', 'has_toctree']
