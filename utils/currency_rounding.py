"""Currency rounding helpers for monetary amounts."""
import decimal
import logging

LOG = logging.getLogger(__name__)

CENTS = decimal.Decimal('0.01')


def round_halves_up(amount, unit=CENTS):
    """Return amount rounded half-up to the given currency unit."""
    value = decimal.Decimal(repr(float(amount)))
    return value.quantize(unit, rounding=decimal.ROUND_HALF_UP)


def round_halves_down(amount, unit=CENTS):
    """Return amount rounded half-down to the given currency unit."""
    value = decimal.Decimal(repr(float(amount)))
    return value.quantize(unit, rounding=decimal.ROUND_HALF_DOWN)


def split_payment(amount, shares):
    """Split amount into shares, giving any remainder to the first share."""
    total = round_halves_up(amount)
    count = int(shares)
    if count <= 0:
        raise ValueError('shares must be positive')
    base = (total / count).quantize(CENTS, rounding=decimal.ROUND_DOWN)
    parts = [base for _ in range(count)]
    parts[0] += total - base * count
    return parts


__all__ = ['round_halves_up', 'round_halves_down', 'split_payment']
