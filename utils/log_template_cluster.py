"""Cluster log messages by replacing variable parts with placeholders.

Raw messages rarely repeat verbatim, but their templates do.  Clustering
by a lightweight token mask gives reliable frequency counts without a
clustering library or a trained model.
"""

import logging
import re
from typing import Dict, Iterable, List

LOG = logging.getLogger(__name__)

NUMBER_PATTERN = re.compile(r"\b\d+(?:\.\d+)?\b")
HEX_PATTERN = re.compile(r"\b[0-9a-fA-F]{8,}\b")
PATH_PATTERN = re.compile(r"(/[\w.-]+){2,}")


def template_of(message: str) -> str:
    """Return a placeholder masked template for a log message."""
    masked = HEX_PATTERN.sub("<hex>", message)
    masked = NUMBER_PATTERN.sub("<num>", masked)
    masked = PATH_PATTERN.sub("<path>", masked)
    return masked.strip()


def cluster(messages: Iterable[str], limit: int = 10) -> List[Dict[str, object]]:
    """Return the most frequent templates with counts and examples."""
    counts: Dict[str, int] = {}
    examples: Dict[str, str] = {}
    for message in messages:
        template = template_of(message)
        counts[template] = counts.get(template, 0) + 1
        examples.setdefault(template, message)
    ordered = sorted(counts.items(), key=lambda item: item[1], reverse=True)[:limit]
    clusters = [{"template": template, "count": count, "example": examples[template]}
                for template, count in ordered]
    LOG.debug("clustered messages into %d template(s)", len(counts))
    return clusters


__all__ = ["template_of", "cluster"]
