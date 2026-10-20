"""Predicate helpers for checking whether an IP address falls inside a CIDR block."""

import ipaddress

LOG = None


def normalize_cidr(cidr_text):
    """Return a strict ipaddress network object or ``None`` when invalid."""
    try:
        return ipaddress.ip_network(cidr_text, strict=True)
    except ValueError:
        return None


def ip_in_cidr(address, cidr_text):
    """Return True when ``address`` is a member of the given CIDR network."""
    net = normalize_cidr(cidr_text)
    if net is None:
        return False
    try:
        return ipaddress.ip_address(address) in net
    except ValueError:
        return False


def containment_reason(address, cidr_text):
    """Classify the containment outcome into a short machine readable code."""
    if normalize_cidr(cidr_text) is None:
        return "bad-network"
    return "inside" if ip_in_cidr(address, cidr_text) else "outside"


__all__ = ["normalize_cidr", "ip_in_cidr", "containment_reason"]
