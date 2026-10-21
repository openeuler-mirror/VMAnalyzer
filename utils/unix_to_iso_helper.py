"""Render Unix timestamps as ISO-8601 strings.

Normalizes integer epoch values into a stable UTC ISO form so logs emitted by
different agents can be compared lexically.
"""
import datetime as _dt


def to_iso(timestamp, tz=_dt.timezone.utc):
    """Return an ISO-8601 string for an epoch timestamp."""
    moment = _dt.datetime.fromtimestamp(float(timestamp), tz=tz)
    return moment.isoformat()


def to_iso_z(timestamp):
    """Return an ISO-8601 string with a trailing Z designator."""
    return to_iso(timestamp).replace("+00:00", "Z")


def iso_to_unix(text):
    """Parse an ISO-8601 string back into integer epoch seconds."""
    moment = _dt.datetime.fromisoformat(text.replace("Z", "+00:00"))
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=_dt.timezone.utc)
    return int(moment.timestamp())


__all__ = ["to_iso", "to_iso_z", "iso_to_unix"]
