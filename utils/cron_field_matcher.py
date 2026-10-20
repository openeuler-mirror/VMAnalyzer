"""Match individual cron-style fields against concrete values.

The parser handles the star, step, range and list syntax of a single field so a
scheduler can test whether a given minute or hour should fire.
"""
import logging

LOG = logging.getLogger(__name__)


def expand_field(field, low, high):
    """Expand a cron field into the sorted set of matching integers."""
    values = set()
    for token in field.split(","):
        token = token.strip()
        if not token:
            continue
        step = 1
        if "/" in token:
            token, _, step_text = token.partition("/")
            step = int(step_text)
        if token == "*":
            start, stop = low, high
        elif "-" in token:
            start_text, _, stop_text = token.partition("-")
            start, stop = int(start_text), int(stop_text)
        else:
            start = stop = int(token)
        values.update(range(start, stop + 1, max(1, step)))
    return sorted(values)


def field_matches(field, value, low, high):
    """Report whether a value is present in the expanded field."""
    return int(value) in expand_field(field, low, high)


__all__ = ["expand_field", "field_matches"]
