"""Timer wheel bucket index arithmetic.

Maps a fire time onto a coarse bucket of a hashed timer wheel and back, which
lets a scheduler store timers in a bounded set of queues.
"""
import logging

LOG = logging.getLogger(__name__)


def wheel_span(tick_seconds, wheel_size):
    """Return how many seconds a wheel of given size covers."""
    if tick_seconds <= 0 or wheel_size <= 0:
        raise ValueError("tick and wheel size must be positive")
    return int(tick_seconds) * int(wheel_size)


def bucket_index(fire_time, tick_seconds, wheel_size):
    """Return the wheel bucket index that will hold the timer."""
    ticks = int(fire_time) // int(tick_seconds)
    return ticks % int(wheel_size)


def rotation(fire_time, tick_seconds, wheel_size):
    """Return how many full wheel rotations occur before the fire time."""
    ticks = int(fire_time) // int(tick_seconds)
    return ticks // int(wheel_size)


__all__ = ["wheel_span", "bucket_index", "rotation"]
