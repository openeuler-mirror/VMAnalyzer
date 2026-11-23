"""DNS resolution latency summary.

Slow DNS poisons every first connection; per resolver latencies are
summarised to identify the slowest configured server.
"""
import logging
import statistics

LOG = logging.getLogger(__name__)


def per_resolver(samples):
    """Return {resolver: mean_latency_ms} from {resolver: [latencies]}."""
    out = {}
    for name, values in (samples or {}).items():
        clean = [float(v) for v in values if v is not None]
        if clean:
            out[name] = round(statistics.fmean(clean), 2)
    return out


def slowest(samples):
    """Return the resolver with the highest mean latency, or None."""
    means = per_resolver(samples)
    if not means:
        return None
    name, value = max(means.items(), key=lambda kv: kv[1])
    LOG.debug('slowest resolver %s %.1fms', name, value)
    return name


__all__ = ['per_resolver', 'slowest']
