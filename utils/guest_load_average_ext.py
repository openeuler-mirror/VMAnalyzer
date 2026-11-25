"""Guest load average normalisation.

Load average is only comparable across guests when divided by the vCPU count
of that guest, so the raw values are normalised per core.
"""
import logging

LOG = logging.getLogger(__name__)


def parse_loadavg(text):
    """Parse the three load averages out of a /proc/loadavg line."""
    fields = str(text or '').split()
    if len(fields) < 3:
        return None
    try:
        return tuple(round(float(fields[i]), 2) for i in range(3))
    except ValueError:
        return None


def per_vcpu(load1, vcpus):
    """Return load1 divided by vCPU count, or None when unknown."""
    if not vcpus or vcpus <= 0:
        return None
    return round(float(load1) / float(vcpus), 3)


def is_saturated(load1, vcpus, watermark=1.0):
    """Report whether per vCPU load crosses the watermark."""
    ratio = per_vcpu(load1, vcpus)
    if ratio is None:
        return False
    LOG.debug('load1 %.2f on %d vcpus', load1, vcpus)
    return ratio >= watermark


__all__ = ['parse_loadavg', 'per_vcpu', 'is_saturated']
