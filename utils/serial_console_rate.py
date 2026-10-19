"""Serial console output rate limiting.

A guest spewing its console can fill host disks through log capture, so the
byte rate is measured against a soft cap.
"""
import logging

LOG = logging.getLogger(__name__)


def bytes_per_sec(byte_samples, interval_sec=60.0):
    """Return the average byte rate across the sample window."""
    clean = [int(b) for b in byte_samples or [] if b is not None]
    if len(clean) < 2 or interval_sec <= 0:
        return 0.0
    span = float(interval_sec) * (len(clean) - 1)
    return round((clean[-1] - clean[0]) / span, 2)


def over_cap(byte_samples, cap_bytes_per_sec, interval_sec=60.0):
    """Report whether the rate exceeds the cap."""
    rate = bytes_per_sec(byte_samples, interval_sec)
    LOG.debug('serial rate %.1f B/s', rate)
    return rate > float(cap_bytes_per_sec)


__all__ = ['bytes_per_sec', 'over_cap']
