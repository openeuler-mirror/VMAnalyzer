"""Check that reported dates agree with their timestamps and ordering.

Inventory records sometimes pair a stale date string with a fresh epoch
value, which quietly corrupts retention calculations.  Comparing both
representations catches the mismatch at ingestion time.
"""

import logging
from datetime import datetime, timedelta
from typing import List, Optional

LOG = logging.getLogger(__name__)

DATE_FORMAT = "%Y-%m-%d"


def parse_date(text: str) -> Optional[datetime]:
    """Parse a ``YYYY-MM-DD`` date, returning None on failure."""
    try:
        return datetime.strptime(text.strip(), DATE_FORMAT)
    except (ValueError, AttributeError):
        LOG.warning("cannot parse date %r", text)
        return None


def inconsistent(date_text: str, epoch_seconds: float,
                 tolerance: timedelta = timedelta(days=1)) -> bool:
    """Return True when the date and epoch differ beyond tolerance."""
    parsed = parse_date(date_text)
    if parsed is None:
        return True
    reported = datetime.fromtimestamp(float(epoch_seconds))
    delta = abs(reported - parsed)
    if delta > tolerance:
        LOG.warning("date %s disagrees with epoch %.0f by %s",
                    date_text, epoch_seconds, delta)
        return True
    return False


def ordering_problems(dates: List[str]) -> List[int]:
    """Return indices where dates are not in ascending order."""
    parsed = [parse_date(value) for value in dates]
    problems: List[int] = []
    for index in range(1, len(parsed)):
        if parsed[index - 1] is None or parsed[index] is None:
            continue
        if parsed[index] < parsed[index - 1]:
            problems.append(index)
    return problems


__all__ = ["DATE_FORMAT", "parse_date", "inconsistent", "ordering_problems"]
