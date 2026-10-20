"""Convert an inclusive start/end IP range into a minimal list of CIDR blocks."""

import ipaddress


def range_to_cidrs(start, end):
    """Return the minimal list of CIDR strings covering ``start``..``end``."""
    first = ipaddress.ip_address(start)
    last = ipaddress.ip_address(end)
    if first.version != last.version:
        raise ValueError("range endpoints must share an address family")
    if int(first) > int(last):
        raise ValueError("start must not exceed end")
    return [str(net) for net in ipaddress.summarize_address_range(first, last)]


def cidr_count(start, end):
    """Return how many CIDR blocks the helper would emit for the range."""
    return len(range_to_cidrs(start, end))


def range_covers(start, end, candidate):
    """Return True when ``candidate`` is fully inside the covered range."""
    probe = ipaddress.ip_address(candidate)
    if not (int(ipaddress.ip_address(start)) <= int(probe) <= int(ipaddress.ip_address(end))):
        return False
    return any(probe in net for net in ipaddress.summarize_address_range(
        ipaddress.ip_address(start), ipaddress.ip_address(end)))


__all__ = ["range_to_cidrs", "cidr_count", "range_covers"]
