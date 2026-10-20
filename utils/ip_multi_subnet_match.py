"""Check membership of an IP address against a list of named subnets."""

import ipaddress


def _networks(subnets):
    """Yield ``(name, network)`` pairs, silently skipping unparseable entries."""
    for name, cidr in subnets:
        try:
            yield name, ipaddress.ip_network(cidr, strict=False)
        except ValueError:
            continue


def match_all_subnets(address, subnets):
    """Return the sorted names of every subnet containing ``address``."""
    try:
        ip = ipaddress.ip_address(address)
    except ValueError:
        return []
    return sorted(name for name, net in _networks(subnets) if ip in net)


def first_matching_subnet(address, subnets, default=None):
    """Return the first subnet name that contains ``address``."""
    hits = match_all_subnets(address, subnets)
    return hits[0] if hits else default


__all__ = ["match_all_subnets", "first_matching_subnet"]
