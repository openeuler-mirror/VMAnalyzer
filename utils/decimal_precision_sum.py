"""High precision summation using the decimal module."""
import decimal
import logging

LOG = logging.getLogger(__name__)

PRECISION = 34


def precise_sum(values, precision=PRECISION):
    """Return the exact decimal sum of a sequence of numbers."""
    context = decimal.Context(prec=int(precision))
    total = decimal.Decimal(0)
    for value in values or []:
        total = context.add(total, context.create_decimal(repr(float(value))))
    return total


def compensated_sum(values):
    """Return a Kahan compensated floating point sum of the sequence."""
    total = 0.0
    compensation = 0.0
    for value in values or []:
        adjusted = float(value) - compensation
        running = total + adjusted
        compensation = (running - total) - adjusted
        total = running
    return total


def sum_error(values):
    """Return the absolute difference between exact and naive summation."""
    naive = sum(float(v) for v in values or [])
    exact = precise_sum(values)
    return abs(decimal.Decimal(repr(naive)) - exact)


__all__ = ['precise_sum', 'compensated_sum', 'sum_error']
