"""Track alert state transitions and compute dwell time per state.

Time spent firing versus acknowledged is the core input for SLA reporting.
Recording only transitions (not every poll) keeps the event log small while
remaining sufficient to reconstruct durations.
"""

import logging
from typing import Dict, Iterable, List, Tuple

LOG = logging.getLogger(__name__)

STATES = ("pending", "firing", "acknowledged", "resolved")


def transitions(events: Iterable[Tuple[str, float]]) -> List[Tuple[str, str, float]]:
    """Return ``(from_state, to_state, timestamp)`` for real changes only."""
    changes: List[Tuple[str, str, float]] = []
    previous = None
    for state, timestamp in events:
        state = str(state).lower()
        if state not in STATES:
            LOG.warning("ignoring unknown alert state %r", state)
            continue
        if previous is not None and state != previous:
            changes.append((previous, state, float(timestamp)))
        previous = state
    return changes


def dwell_times(events: Iterable[Tuple[str, float]]) -> Dict[str, float]:
    """Sum the seconds spent in each state."""
    materialised = sorted(events, key=lambda item: item[1])
    totals: Dict[str, float] = {state: 0.0 for state in STATES}
    for index in range(len(materialised) - 1):
        state, timestamp = materialised[index]
        following = materialised[index + 1][1]
        if state in totals:
            totals[state] += max(0.0, float(following) - float(timestamp))
    LOG.debug("dwell totals %s", totals)
    return totals


def mean_time_to_resolve(events: Iterable[Tuple[str, float]]) -> float:
    """Return the total firing time divided by the number of resolutions."""
    materialised = list(events)
    dwell = dwell_times(materialised)
    resolutions = sum(1 for state, _ in transitions(materialised) if state == "resolved")
    return round(dwell.get("firing", 0.0) / resolutions, 2) if resolutions else 0.0


__all__ = ["STATES", "transitions", "dwell_times", "mean_time_to_resolve"]
