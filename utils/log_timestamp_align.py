"""Align log timestamps expressed in mixed formats to epoch seconds.

Logs merged from syslog, journald and guest agents carry different
timestamp formats.  Normalising them to epoch seconds is a prerequisite for
correct ordering and for correlating events across sources.
"""

import logging
from datetime import datetime
from typing import List, Optional

LOG = logging.getLogger(__name__)

ACCEPTED_FORMATS = (
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d %H:%M:%S",
    "%b %d %H:%M:%S",
    "%d/%m/%Y %H:%M:%S",
)


def parse_timestamp(text: str, reference_year: Optional[int] = None) -> Optional[float]:
    """Return epoch seconds for a recognised timestamp, else None."""
    cleaned = text.strip()
    try:
        return float(cleaned)
    except ValueError:
        pass
    if cleaned.endswith("Z"):
        cleaned = cleaned[:-1]
    for pattern in ACCEPTED_FORMATS:
        try:
            parsed = datetime.strptime(cleaned, pattern)
        except ValueError:
            continue
        if pattern == "%b %d %H:%M:%S":
            parsed = parsed.replace(year=reference_year or datetime.now().year)
        return parsed.timestamp()
    LOG.warning("unrecognised log timestamp %r", text)
    return None


def align(texts: List[str], reference_year: Optional[int] = None) -> List[float]:
    """Convert parseable timestamps, dropping the rest, and sort them."""
    values = [parse_timestamp(text, reference_year) for text in texts]
    aligned = sorted(value for value in values if value is not None)
    LOG.debug("aligned %d of %d log timestamp(s)", len(aligned), len(texts))
    return aligned


__all__ = ["ACCEPTED_FORMATS", "parse_timestamp", "align"]
