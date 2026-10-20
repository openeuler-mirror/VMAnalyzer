"""Banker's rounding and decimal quantisation helpers.

Round-half-to-even avoids the upward bias of the half-up rule when many values
sit exactly on a rounding boundary, which matters for idempotent reporting.
"""
import decimal
import logging

LOG = logging.getLogger(__name__)


def round_half_even(value, places=0):
    """Return value rounded half-to-even at the given decimal places."""
    quantum = decimal.Decimal(1).scaleb(-places)
    return decimal.Decimal(repr(float(value))).quantize(
        quantum, rounding=decimal.ROUND_HALF_EVEN)


def round_half_up(value, places=0):
    """Return value rounded half-up at the given decimal places."""
    quantum = decimal.Decimal(1).scaleb(-places)
    return decimal.Decimal(repr(float(value))).quantize(
        quantum, rounding=decimal.ROUND_HALF_UP)


def quantize_series(values, places=0):
    """Return every sample rounded half-to-even to the given places."""
    return [round_half_even(v, places) for v in values or []]


__all__ = ['round_half_even', 'round_half_up', 'quantize_series']
