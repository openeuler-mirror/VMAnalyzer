"""Lenient ISO-8601 timestamp parsing.

Parses the common ISO-8601 spellings produced by monitoring agents without
pulling in a full date library, returning timezone aware datetimes.
"""
import datetime as _dt


def parse_iso8601(text):
    """Parse an ISO-8601 string, tolerating a trailing Z designator."""
    value = text.strip()
    if value.endswith("Z") or value.endswith("z"):
        value = value[:-1] + "+00:00"
    return _dt.datetime.fromisoformat(value)


def to_epoch_seconds(text):
    """Convert an ISO-8601 string into integer epoch seconds."""
    parsed = parse_iso8601(text)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=_dt.timezone.utc)
    return int(parsed.timestamp())


__all__ = ["parse_iso8601", "to_epoch_seconds"]
