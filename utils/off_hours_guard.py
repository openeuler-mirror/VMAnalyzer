"""Guard actions during off-hours windows.

Given a daily closed window such as 22:00-06:00 the guard decides whether the
current wall clock time sits inside it, handling the midnight wrap.
"""
SECONDS_PER_DAY = 86400


def in_off_hours(second_of_day, start_second, end_second):
    """Report whether a second-of-day falls inside the off-hours window."""
    moment = int(second_of_day) % SECONDS_PER_DAY
    start = int(start_second) % SECONDS_PER_DAY
    end = int(end_second) % SECONDS_PER_DAY
    if start <= end:
        return start <= moment < end
    return moment >= start or moment < end


def window_length(start_second, end_second):
    """Return the length of the off-hours window in seconds."""
    start = int(start_second) % SECONDS_PER_DAY
    end = int(end_second) % SECONDS_PER_DAY
    span = (end - start) % SECONDS_PER_DAY
    return span or SECONDS_PER_DAY


def next_allowed(second_of_day, end_second):
    """Return the seconds until off-hours end from the given moment."""
    moment = int(second_of_day) % SECONDS_PER_DAY
    end = int(end_second) % SECONDS_PER_DAY
    return (end - moment) % SECONDS_PER_DAY


__all__ = ["in_off_hours", "window_length", "next_allowed"]
