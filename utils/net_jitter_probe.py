"""Network jitter measurement from round trip samples.

Jitter is the variation of latency rather than its absolute value, and it is
what breaks real time traffic.  These helpers compute mean deviation and a
packet delay variation indicator.
"""
import statistics


def mean_jitter(samples_ms):
    """Return the mean absolute successive difference of RTT samples."""
    values = [float(s) for s in samples_ms or [] if s is not None]
    if len(values) < 2:
        return 0.0
    diffs = [abs(values[i] - values[i - 1]) for i in range(1, len(values))]
    return round(statistics.fmean(diffs), 3)


def packet_delay_variation(samples_ms):
    """Return the RFC 3550 style interarrival jitter estimate."""
    values = [float(s) for s in samples_ms or [] if s is not None]
    if not values:
        return 0.0
    jitter = 0.0
    for i in range(1, len(values)):
        d = abs(values[i] - values[i - 1])
        jitter += (d - jitter) / 16.0
    return round(jitter, 3)


def jitter_verdict(jitter_ms, warn_ms=30.0, crit_ms=100.0):
    """Classify jitter as stable, degraded or unstable."""
    if jitter_ms >= crit_ms:
        return 'unstable'
    if jitter_ms >= warn_ms:
        return 'degraded'
    return 'stable'


__all__ = ['mean_jitter', 'packet_delay_variation', 'jitter_verdict']
