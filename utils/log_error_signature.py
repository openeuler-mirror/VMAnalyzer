"""Derive compact error signatures for grouping related failures.

Stack traces and error messages vary in line numbers and paths, which hides
the underlying repetition.  Extracting the exception type plus the first
stable sentence yields a signature suitable for counting and alerting.
"""

import logging
import re
from typing import Iterable, List, Tuple

LOG = logging.getLogger(__name__)

EXCEPTION_PATTERN = re.compile(r"\b([A-Z][A-Za-z0-9_]*(?:Error|Exception|Warning|Timeout))\b")
NUMBER_PATTERN = re.compile(r"\b\d+\b")


def signature_of(message: str) -> str:
    """Return the exception type plus a number-masked message prefix."""
    exception_match = EXCEPTION_PATTERN.search(message)
    kind = exception_match.group(1) if exception_match else "Unclassified"
    body = NUMBER_PATTERN.sub("#", message).strip()
    body = body.split(".")[0][:120]
    return "{}: {}".format(kind, body)


def group_messages(messages: Iterable[str]) -> List[Tuple[str, int]]:
    """Return signatures ordered by descending occurrence count."""
    counts = {}
    for message in messages:
        signature = signature_of(message)
        counts[signature] = counts.get(signature, 0) + 1
    ordered = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    LOG.debug("reduced messages to %d signature(s)", len(ordered))
    return ordered


def top_signature(messages: Iterable[str]) -> str:
    """Return the most common signature, or an empty string."""
    ordered = group_messages(messages)
    return ordered[0][0] if ordered else ""


__all__ = ["EXCEPTION_PATTERN", "signature_of", "group_messages", "top_signature"]
