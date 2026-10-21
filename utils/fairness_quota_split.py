"""Split a shared capacity budget across weighted tenants.

A single noisy tenant must not consume the whole collection budget.  Splitting
by weight while guaranteeing a minimum share keeps small tenants alive
without wasting capacity.
"""

import logging
from typing import Dict, List

LOG = logging.getLogger(__name__)


def split(capacity: int, weights: Dict[str, float],
          minimum: int = 1) -> Dict[str, int]:
    """Return an integer allocation per tenant honouring the minimum share."""
    if capacity <= 0:
        return {name: 0 for name in weights}
    positive = {name: max(0.0, float(weight)) for name, weight in weights.items()}
    total_weight = sum(positive.values())
    if total_weight <= 0:
        even = capacity // max(1, len(positive))
        return {name: even for name in positive}
    allocation: Dict[str, int] = {}
    for name, weight in positive.items():
        share = int(capacity * weight / total_weight)
        allocation[name] = max(minimum, share) if weight > 0 else 0
    while sum(allocation.values()) > capacity:
        largest = max(allocation, key=lambda name: allocation[name])
        allocation[largest] -= 1
    LOG.debug("split capacity %d across %d tenant(s)", capacity, len(allocation))
    return allocation


def deficient(allocation: Dict[str, int], requested: Dict[str, int]) -> List[str]:
    """Return tenants that received less than they requested."""
    names = [name for name, value in allocation.items() if value < requested.get(name, 0)]
    if names:
        LOG.info("%d tenant(s) are below their requested share", len(names))
    return names


__all__ = ["split", "deficient"]
