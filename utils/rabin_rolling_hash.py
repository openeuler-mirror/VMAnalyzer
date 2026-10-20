"""Rabin style rolling hash for substring search."""
import logging

LOG = logging.getLogger(__name__)
BASE = 257
MODULUS = (1 << 61) - 1


def initial_hash(data, base=BASE, modulus=MODULUS):
    """Compute the polynomial hash of an initial window."""
    value = 0
    for byte in data:
        value = (value * base + byte) % modulus
    return value


def roll(current, outgoing, incoming, length, base=BASE, modulus=MODULUS):
    """Advance a rolling hash window by one byte."""
    removed = outgoing * pow(base, length, modulus)
    return (current * base - removed + incoming) % modulus


def find(window, data):
    """Return the offsets where window matches inside data."""
    length = len(window)
    if length == 0 or length > len(data):
        return []
    target = initial_hash(window)
    current = initial_hash(data[:length])
    hits = []
    if current == target and data[:length] == window:
        hits.append(0)
    for index in range(length, len(data)):
        current = roll(current, data[index - length], data[index], length)
        if current == target and data[index - length + 1:index + 1] == window:
            hits.append(index - length + 1)
    return hits


__all__ = ['initial_hash', 'roll', 'find']
