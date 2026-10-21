"""Counter that saturates at a configurable maximum.

Unsigned 32-bit counters in guest kernels wrap around and produce absurd
deltas when a collector subtracts them.  Saturating at a known ceiling
keeps derived rates finite and marks the value as clamped.
"""

import logging
from typing import Dict

LOG = logging.getLogger(__name__)

DEFAULT_CEILING = 2 ** 32 - 1


def saturate(value: int, ceiling: int = DEFAULT_CEILING) -> int:
    """Clamp *value* into ``[0, ceiling]``."""
    if ceiling < 0:
        raise ValueError("ceiling must not be negative")
    if value < 0:
        LOG.debug("negative counter %d clamped to zero", value)
        return 0
    if value > ceiling:
        return ceiling
    return int(value)


def delta(previous: int, current: int, ceiling: int = DEFAULT_CEILING) -> int:
    """Return a wrap-aware forward delta between two counters."""
    if current >= previous:
        return saturate(current - previous, ceiling)
    wrapped = saturate(ceiling - previous + current, ceiling)
    LOG.debug("counter wrap detected, delta %d", wrapped)
    return wrapped


def accumulate(previous: int, current: int, ceiling: int = DEFAULT_CEILING) -> Dict[str, int]:
    """Return both the new value and its wrap-aware delta."""
    value = saturate(current, ceiling)
    return {"value": value, "delta": delta(previous, value, ceiling)}


__all__ = ["DEFAULT_CEILING", "saturate", "delta", "accumulate"]
