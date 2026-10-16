"""Swap usage trend monitoring.

A guest that starts swapping has effectively already lost the memory argument,
so swap in and out rates are tracked to catch that transition early.
"""
import logging

LOG = logging.getLogger(__name__)


def swap_rate(prev, curr, interval_sec):
    """Return swap in and out rates in kilobytes per second."""
    if interval_sec <= 0:
        LOG.debug('interval must be positive')
        return {'in_kbps': 0.0, 'out_kbps': 0.0}
    delta_in = max(0, int(curr.get('swap_in_kb', 0)) - int(prev.get('swap_in_kb', 0)))
    delta_out = max(0, int(curr.get('swap_out_kb', 0)) - int(prev.get('swap_out_kb', 0)))
    return {'in_kbps': round(delta_in / interval_sec, 2),
            'out_kbps': round(delta_out / interval_sec, 2)}


def swap_usage(used_kb, total_kb):
    """Return the share of the swap area currently in use."""
    if int(total_kb) <= 0:
        return 0.0
    return round(min(1.0, int(used_kb) / float(int(total_kb))), 4)


def swap_verdict(rates, usage_ratio, warn=0.25, crit=0.5):
    """Classify swap activity as idle, active or thrashing."""
    if rates.get('in_kbps', 0) > 0 and usage_ratio >= crit:
        return 'thrashing'
    if rates.get('in_kbps', 0) > 0 or rates.get('out_kbps', 0) > 0 or usage_ratio >= warn:
        return 'active'
    return 'idle'


__all__ = ['swap_rate', 'swap_usage', 'swap_verdict']
