"""Count seconds inside a daily business-hours window.

Given a window such as 09:00-17:00 the helper measures how much of a real
interval overlaps the open part of the day, ignoring the overnight gap.
"""
BUSINESS_START_HOUR = 9
BUSINESS_END_HOUR = 17


def day_window_seconds():
    """Return the length of the business window in seconds."""
    return (BUSINESS_END_HOUR - BUSINESS_START_HOUR) * 3600


def overlap_seconds(start_second, end_second):
    """Return business seconds covered by a same-day time range."""
    if end_second <= start_second:
        return 0
    open_at = BUSINESS_START_HOUR * 3600
    close_at = BUSINESS_END_HOUR * 3600
    low = max(open_at, int(start_second))
    high = min(close_at, int(end_second))
    return max(0, high - low)


def within_business_hours(second_of_day):
    """Report whether a second-of-day falls inside the window."""
    return BUSINESS_START_HOUR * 3600 <= second_of_day < BUSINESS_END_HOUR * 3600


__all__ = ["day_window_seconds", "overlap_seconds", "within_business_hours"]
