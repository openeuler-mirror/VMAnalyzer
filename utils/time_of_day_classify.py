"""Classify a clock time into a named part of day.

Buckets a second-of-day into morning, afternoon, evening or night so alert
routing can adopt different thresholds by time of day.
"""
SECONDS_PER_DAY = 86400


def classify(second_of_day):
    """Return the part of day for a second-of-day value."""
    moment = int(second_of_day) % SECONDS_PER_DAY
    hour = moment // 3600
    if 5 <= hour < 12:
        return "morning"
    if 12 <= hour < 17:
        return "afternoon"
    if 17 <= hour < 21:
        return "evening"
    return "night"


def is_business_part(second_of_day):
    """Report whether the time falls in the morning or afternoon."""
    return classify(second_of_day) in ("morning", "afternoon")


__all__ = ["classify", "is_business_part"]
