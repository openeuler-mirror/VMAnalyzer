"""Parse ``virsh domstats`` key-value output into typed records.

domstats prints ``domain.state.0=...`` style keys whose depth varies by
libvirt version.  A generic dotted-key parser plus numeric coercion yields
a usable mapping without hard-coding version specific layouts.
"""

import logging
from typing import Dict, Iterable, Union

LOG = logging.getLogger(__name__)

Number = Union[int, float]


def coerce_value(text: str) -> Union[str, Number]:
    """Convert numeric-looking values while leaving enums as strings."""
    lowered = text.strip()
    if lowered.lower() in {"yes", "true"}:
        return "yes"
    if lowered.lower() in {"no", "false"}:
        return "no"
    try:
        return int(lowered)
    except ValueError:
        pass
    try:
        return float(lowered)
    except ValueError:
        return lowered


def parse_domstats(lines: Iterable[str]) -> Dict[str, Dict[str, object]]:
    """Group domstats output by domain, then by dotted key."""
    domains: Dict[str, Dict[str, object]] = {}
    for line in lines:
        key, separator, value = line.strip().partition("=")
        if not separator:
            continue
        parts = key.strip().split(".")
        if len(parts) < 3 or parts[0] != "domain":
            continue
        name = parts[1]
        field = ".".join(parts[2:])
        domains.setdefault(name, {})[field] = coerce_value(value)
    LOG.debug("parsed domstats for %d domain(s)", len(domains))
    return domains


def numeric_field(domain: Dict[str, object], field: str, default: float = 0.0) -> float:
    """Return a numeric field, substituting *default* when absent."""
    value = domain.get(field)
    return float(value) if isinstance(value, (int, float)) else default


__all__ = ["Number", "coerce_value", "parse_domstats", "numeric_field"]
