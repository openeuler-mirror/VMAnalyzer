"""OpenTelemetry span statistics.

Per-trace span counts and error ratios show whether instrumentation
overhead and error rates stay within budget.
"""
import logging

LOG = logging.getLogger(__name__)


def spans_per_trace(spans):
    """Return {trace_id: span count}."""
    counts = {}
    for span in spans or []:
        tid = span.get('trace_id')
        counts[tid] = counts.get(tid, 0) + 1
    return counts


def error_ratio(spans):
    """Return the fraction of spans with error status."""
    total = len(spans or [])
    if total == 0:
        return 0.0
    errors = sum(1 for s in spans if s.get('status') == 'ERROR')
    LOG.debug('otel error ratio %d/%d', errors, total)
    return round(errors / float(total), 4)


__all__ = ['spans_per_trace', 'error_ratio']
