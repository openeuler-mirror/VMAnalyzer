"""Render uptime and boot ages.

Boot timestamps are noisy, so these helpers turn a raw boot time into a stable
uptime string and a coarse bucket suitable for grouping hosts.
"""
UPTIME_BUCKETS = (
    ("weeks", 604800),
    ("days", 86400),
    ("hours", 3600),
    ("minutes", 60),
)


def uptime_seconds(boot_time, now):
    """Return the uptime in seconds, clamping clock skew to zero."""
    return max(0.0, now - boot_time)


def format_uptime(boot_time, now):
    """Render the two leading components of an uptime value."""
    remaining = int(uptime_seconds(boot_time, now))
    parts = []
    for label, size in UPTIME_BUCKETS:
        amount, remaining = divmod(remaining, size)
        if amount:
            parts.append("%d %s" % (amount, label))
    return ", ".join(parts[:2]) if parts else "0 minutes"


__all__ = ["uptime_seconds", "format_uptime"]
