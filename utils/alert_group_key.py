"""Build stable grouping keys from alert label sets.

Grouping alerts by a subset of labels collapses correlated pages without
losing the reason.  Missing labels are represented explicitly so keys stay
unambiguous instead of silently merging unrelated groups.
"""

import logging
from typing import Dict, List, Sequence

LOG = logging.getLogger(__name__)


def group_key(labels: Dict[str, str], fields: Sequence[str]) -> str:
    """Return a canonical ``field=value`` key for the requested labels."""
    parts: List[str] = []
    for field in fields:
        value = labels.get(field)
        parts.append("{}={}".format(field, value if value is not None else "-"))
    key = "|".join(parts)
    LOG.debug("built alert group key %s", key)
    return key


def common_labels(alerts: List[Dict[str, str]]) -> Dict[str, str]:
    """Return labels whose values agree across every alert."""
    if not alerts:
        return {}
    shared: Dict[str, str] = {}
    for name, value in alerts[0].items():
        if all(alert.get(name) == value for alert in alerts[1:]):
            shared[name] = value
    return shared


def distinct_values(alerts: List[Dict[str, str]], field: str) -> List[str]:
    """Return the sorted distinct values of a label across alerts."""
    values = {alert.get(field) for alert in alerts if alert.get(field) is not None}
    return sorted(values)


__all__ = ["group_key", "common_labels", "distinct_values"]
