"""Writeback throttle engagement.

When the kernel throttles writers, dirty pages piled up; engagement time is
turned into a duty cycle percentage.
"""
import logging

LOG = logging.getLogger(__name__)


def duty_cycle(throttled_ms, window_ms):
    """Return the share of the window spent throttled in 0..1."""
    if not window_ms or window_ms <= 0:
        return 0.0
    return round(min(1.0, max(0.0, float(throttled_ms or 0) / float(window_ms))), 3)


def verdict(duty, ceiling=0.1):
    """Classify the duty cycle as normal or heavy."""
    verdict = 'heavy' if duty >= ceiling else 'normal'
    LOG.debug('writeback duty %.3f -> %s', duty, verdict)
    return verdict


__all__ = ['duty_cycle', 'verdict']
