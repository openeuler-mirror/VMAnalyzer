"""ISO week helpers.

Provides the ISO year, week and weekday triple plus a formatter that renders
the canonical YYYY-Www label used in weekly reports.
"""
import datetime as _dt


def iso_parts(day):
    """Return the (iso_year, iso_week, iso_weekday) triple for a date."""
    year, week, weekday = day.isocalendar()[:3]
    return int(year), int(week), int(weekday)


def week_label(day):
    """Render the canonical ISO week label for a date."""
    year, week, _ = iso_parts(day)
    return "%04d-W%02d" % (year, week)


def weeks_between(start, end):
    """Return the number of ISO week boundaries between two dates."""
    return end.isocalendar()[1] - start.isocalendar()[1]


__all__ = ["iso_parts", "week_label", "weeks_between"]
