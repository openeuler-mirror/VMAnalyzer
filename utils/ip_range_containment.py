"""CIDR containment checks for addresses seen in agent telemetry.

Verifying that a reported address falls inside an expected range separates
inventory noise from genuinely unexpected peers on the network.
"""
import ipaddress
import logging

LOG = logging.getLogger(__name__)


def parse_network(cidr):
    """Return an ipaddress network object for a CIDR string, or None."""
    try:
        return ipaddress.ip_network(str(cidr), strict=False)
    except ValueError:
        LOG.debug('invalid cidr %s', cidr)
        return None


def contains(cidr, address):
    """Report whether the address belongs to the CIDR range."""
    network = parse_network(cidr)
    if network is None:
        return False
    try:
        return ipaddress.ip_address(str(address)) in network
    except ValueError:
        return False


def first_containing(address, cidrs):
    """Return the first range from the list that contains the address."""
    for cidr in cidrs or []:
        if contains(cidr, address):
            return cidr
    return None


__all__ = ['parse_network', 'contains', 'first_containing']
