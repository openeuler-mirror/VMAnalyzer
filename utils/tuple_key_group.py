"""Group records by a subset of keys while preserving encounter order.

Report builders frequently need "group rows by host then VM" semantics.
Using a dict of lists preserves the first-seen order, which keeps generated
tables stable between runs without an explicit sort.
"""

import logging
from typing import Dict, Iterable, List, Sequence, Tuple

LOG = logging.getLogger(__name__)


def group_records(records: Iterable[dict], keys: Sequence[str]) -> Dict[Tuple, List[dict]]:
    """Group mappings by the tuple of values at *keys*."""
    groups: Dict[Tuple, List[dict]] = {}
    for record in records:
        signature = tuple(record.get(key) for key in keys)
        groups.setdefault(signature, []).append(record)
    LOG.debug("grouped into %d bucket(s) by %d key(s)", len(groups), len(keys))
    return groups


def group_sizes(records: Iterable[dict], keys: Sequence[str]) -> Dict[Tuple, int]:
    """Return only the size of each group."""
    return {signature: len(items) for signature, items in group_records(records, keys).items()}


def largest_group(records: Iterable[dict], keys: Sequence[str]) -> Tuple:
    """Return the signature of the largest group, or an empty tuple."""
    sizes = group_sizes(records, keys)
    if not sizes:
        return ()
    return max(sizes.items(), key=lambda item: item[1])[0]


__all__ = ["group_records", "group_sizes", "largest_group"]
