"""Parse the Retry-After header, supporting both delay-seconds and HTTP dates."""

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime


def parse_retry_after(value):
    """Return the delay in seconds, a datetime, or ``None`` when unparseable."""
    token = (value or "").strip()
    if not token:
        return None
    if token.isdigit():
        return int(token)
    try:
        return parsedate_to_datetime(token)
    except (TypeError, ValueError):
        return None


def retry_delay_seconds(value, now=None):
    """Return the wait time in integer seconds, or ``None`` when unknown."""
    parsed = parse_retry_after(value)
    if parsed is None:
        return None
    if isinstance(parsed, int):
        return parsed
    reference = now or datetime.now(timezone.utc)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return max(0, int((parsed - reference).total_seconds()))


def should_retry(value, now=None, ceiling=3600):
    """Return True when the advised delay is within an acceptable ceiling."""
    delay = retry_delay_seconds(value, now)
    return delay is not None and 0 <= delay <= ceiling


__all__ = ["parse_retry_after", "retry_delay_seconds", "should_retry"]
