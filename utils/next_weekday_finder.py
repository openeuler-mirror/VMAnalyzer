"""Find upcoming weekdays of a chosen kind.

Given a target weekday number the helper returns the next occurrence and can
also enumerate the next few occurrences for scheduling previews.
"""
import datetime as _dt


def next_weekday(day, target_weekday):
    """Return the next date whose weekday equals the target."""
    if not 0 <= target_weekday <= 6:
        raise ValueError("weekday must be between 0 and 6")
    ahead = (target_weekday - day.weekday()) % 7
    ahead = ahead or 7
    return day + _dt.timedelta(days=ahead)


def upcoming_weekdays(day, target_weekday, count):
    """Return the next count occurrences of the target weekday."""
    result = []
    current = day
    for _ in range(max(0, count)):
        current = next_weekday(current, target_weekday)
        result.append(current)
    return result


__all__ = ["next_weekday", "upcoming_weekdays"]
