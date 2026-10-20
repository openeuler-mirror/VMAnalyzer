"""Arithmetic helpers over dotted-quad subnet masks and prefix lengths."""

import ipaddress


def prefix_to_mask(prefix, version=4):
    """Return the dotted mask string for a prefix length."""
    bits = 32 if version == 4 else 128
    if not 0 <= prefix <= bits:
        raise ValueError("prefix out of range")
    net = ipaddress.ip_network(("0.0.0.0/{}" if version == 4 else "::/{}").format(prefix))
    return str(net.netmask)


def mask_to_prefix(mask_text, version=4):
    """Return the prefix length encoded by a contiguous subnet mask."""
    bits = 32 if version == 4 else 128
    value = int(ipaddress.ip_address(mask_text))
    binary = format(value, "0{}b".format(bits))
    if "01" in binary:
        raise ValueError("mask is not contiguous")
    return binary.count("1")


def usable_host_count(prefix, version=4):
    """Return the number of assignable hosts for a prefix length."""
    bits = 32 if version == 4 else 128
    if prefix >= bits - 1:
        return 0
    return 2 ** (bits - prefix) - 2


__all__ = ["prefix_to_mask", "mask_to_prefix", "usable_host_count"]
