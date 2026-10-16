"""Guest uptime and unexpected reboot detection.

A boot time that moves forward unexpectedly means the guest restarted, which
invalidates long lived counters and can indicate a host level fault.  These
helpers normalise boot timestamps and detect restarts.
"""
from datetime import datetime, timezone
import logging

LOG = logging.getLogger(__name__)


def parse_boot_time(value):
    """Parse an ISO 8601 boot timestamp into an aware UTC datetime."""
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc)
    text = str(value).replace('Z', '+00:00')
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def detect_reboot(previous_boot, current_boot):
    """Report whether the observed boot time indicates a restart."""
    prev = parse_boot_time(previous_boot)
    curr = parse_boot_time(current_boot)
    if curr > prev:
        LOG.info('boot time advanced, guest restarted')
        return True
    return False


def uptime_seconds(boot_time, reference=None):
    """Return the guest uptime in seconds relative to a reference instant."""
    boot = parse_boot_time(boot_time)
    now = reference if reference is not None else datetime.now(timezone.utc)
    return max(0.0, (now - boot).total_seconds())


__all__ = ['parse_boot_time', 'detect_reboot', 'uptime_seconds']
