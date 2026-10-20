"""Two-sample Kolmogorov-Smirnov test.

The largest gap between two empirical CDFs measures whether two metric
distributions genuinely differ after a deploy.
"""
import logging
import math

LOG = logging.getLogger(__name__)


def ks_statistic(sample_a, sample_b):
    """Return the supremum distance between the two ECDFs."""
    a, b = sorted(sample_a or []), sorted(sample_b or [])
    if not a or not b:
        return 0.0
    i = j = 0
    cdf_a = cdf_b = 0.0
    best = 0.0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            i += 1
            cdf_a = i / len(a)
        else:
            j += 1
            cdf_b = j / len(b)
        best = max(best, abs(cdf_a - cdf_b))
    LOG.debug('ks statistic %.4f', best)
    return round(best, 4)


def p_approx(sample_a, sample_b):
    """Return an approximate p-value for the KS statistic."""
    n = len(sample_a or [])
    m = len(sample_b or [])
    if not n or not m:
        return 1.0
    en = math.sqrt(n * m / float(n + m))
    lam = (en + 0.12 + 0.11 / en) * ks_statistic(sample_a, sample_b)
    return max(0.0, min(1.0, 2.0 * math.exp(-2 * lam * lam)))


__all__ = ['ks_statistic', 'p_approx']
