"""Block elevator audit.

Rotational devices benefit from mq-deadline while NVMe prefers none, so the
reported scheduler is checked against the device type.
"""
import logging

LOG = logging.getLogger(__name__)

ROTATIONAL_OK = {'mq-deadline', 'bfq'}
FLASH_OK = {'none', 'mq-deadline'}


def expected(scheduler, rotational):
    """Report whether the scheduler suits the device type."""
    ok = scheduler in (ROTATIONAL_OK if rotational else FLASH_OK)
    LOG.debug('scheduler %s rotational=%s ok=%s', scheduler, rotational, ok)
    return ok


def recommend(rotational):
    """Return the recommended scheduler for the device type."""
    return 'mq-deadline' if rotational else 'none'


__all__ = ['expected', 'recommend']
