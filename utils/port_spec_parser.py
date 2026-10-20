"""Parse textual port specifications such as ``80,443,8000-8100`` into ranges."""

import re

_TOKEN = re.compile(r"^\s*(\d{1,5})\s*(?:-\s*(\d{1,5})\s*)?$")


def parse_port_spec(spec):
    """Return a list of inclusive ``(low, high)`` tuples, skipping bad tokens."""
    spans = []
    for token in spec.split(","):
        match = _TOKEN.match(token)
        if not match:
            continue
        low = int(match.group(1))
        high = int(match.group(2)) if match.group(2) else low
        if 0 <= low <= high <= 65535:
            spans.append((low, high))
    return sorted(spans, key=lambda pair: pair[0])


def expand_ports(spec, limit=4096):
    """Expand a port specification into a sorted unique list of integers."""
    values = set()
    for low, high in parse_port_spec(spec):
        for port in range(low, high + 1):
            values.add(port)
            if len(values) >= limit:
                return sorted(values)
    return sorted(values)


def port_spec_size(spec):
    """Return the total number of ports addressed by the specification."""
    return sum(high - low + 1 for low, high in parse_port_spec(spec))


__all__ = ["parse_port_spec", "expand_ports", "port_spec_size"]
