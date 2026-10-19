"""PCI passthrough configuration audit.

A device handed to a guest must be detached from host drivers and bound to
vfio-pci, so the driver binding of every passthrough target is checked.
"""
import logging

LOG = logging.getLogger(__name__)

REQUIRED_DRIVER = 'vfio-pci'


def audit_bindings(bindings):
    """Return devices bound to the wrong driver from {device: driver}."""
    wrong = {dev: drv for dev, drv in (bindings or {}).items() if drv != REQUIRED_DRIVER}
    if wrong:
        LOG.debug('%d misbound passthrough devices', len(wrong))
    return wrong


def ready_devices(bindings):
    """Return the devices correctly bound to vfio-pci."""
    return sorted(dev for dev, drv in (bindings or {}).items() if drv == REQUIRED_DRIVER)


def audit_report(bindings):
    """Return a summary dict with total, ready and misbound counts."""
    total = len(bindings or {})
    ready = len(ready_devices(bindings))
    return {'total': total, 'ready': ready, 'misbound': total - ready}


__all__ = ['audit_bindings', 'ready_devices', 'audit_report']
