"""Count sign changes in a metric series to estimate oscillation.

Frequent zero crossings in CPU or memory series usually indicate unstable
workloads or a control loop hunting around its target.  Counting crossings
is a cheap oscillation proxy that needs no FFT.
"""

import logging
from typing import Iterable, List, Tuple

LOG = logging.getLogger(__name__)


def _sign(value: float, epsilon: float) -> int:
    """Return -1, 0 or 1 depending on the value relative to epsilon."""
    if value > epsilon:
        return 1
    if value < -epsilon:
        return -1
    return 0


def zero_crossings(values: Iterable[float], epsilon: float = 0.0) -> int:
    """Count transitions between strictly positive and negative values."""
    previous = 0
    crossings = 0
    for value in values:
        sign = _sign(float(value), epsilon)
        if sign == 0:
            continue
        if previous and sign != previous:
            crossings += 1
        previous = sign
    LOG.debug("counted %d zero crossings", crossings)
    return crossings


def crossing_positions(values: Iterable[float], epsilon: float = 0.0) -> List[Tuple[int, int]]:
    """Return (previous-sign, new-sign) for each crossing position."""
    previous = 0
    positions: List[Tuple[int, int]] = []
    for number, value in enumerate(values, start=1):
        sign = _sign(float(value), epsilon)
        if sign == 0:
            continue
        if previous and sign != previous:
            positions.append((previous, sign))
        previous = sign
    return positions


__all__ = ["zero_crossings", "crossing_positions"]
