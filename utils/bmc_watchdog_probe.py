"""BMC watchdog pre-timeout.

Watchdogs reset the host unless the agent pets them; remaining time versus
the pet interval shows the risk.
"""
import logging

LOG = logging.getLogger(__name__)


def safe_margin(remaining_sec, pet_interval_sec):
    """Return remaining/pet-interval; below one means risk."""
    if not pet_interval_sec or pet_interval_sec <= 0:
        return float('inf')
    margin = float(remaining_sec or 0) / float(pet_interval_sec)
    LOG.debug('watchdog margin %.2f', margin)
    return round(margin, 2)


def pet_now(remaining_sec, pet_interval_sec, factor=2.0):
    """Report when remaining time dropped below factor pet intervals."""
    return safe_margin(remaining_sec, pet_interval_sec) < factor


__all__ = ['safe_margin', 'pet_now']
