"""Timestamp normalisation across guest time zones.

Guests report local time while the collector stores UTC, so mixed offsets must
be normalised before ordering or correlation is attempted.
"""
from datetime import datetime, timezone
import logging

LOG = logging.getLogger(__name__)


def _parse(value):
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(str(value).replace('Z', '+00:00'))


def to_utc(value, assume_tz=timezone.utc):
    """Convert a timestamp into an aware UTC datetime."""
    parsed = _parse(value)
    if parsed.tzinfo is None:
        LOG.debug('naive timestamp assumed to use %s', assume_tz)
        parsed = parsed.replace(tzinfo=assume_tz)
    return parsed.astimezone(timezone.utc)


def rebase_series(values, assume_tz=timezone.utc):
    """Convert every timestamp of a series into UTC epoch seconds."""
    return [to_utc(value, assume_tz).timestamp() for value in values or []]


def offsets_only(values):
    """Return the distinct UTC offsets declared in a series."""
    seen = set()
    for value in values or []:
        offset = _parse(value).utcoffset()
        seen.add(offset.total_seconds() if offset else 0.0)
    return sorted(seen)


__all__ = ['to_utc', 'rebase_series', 'offsets_only']
