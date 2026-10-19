"""Tally of KVM vmexit reasons.

A sudden rise in a specific exit reason such as EPT_MISCONFIG points at a
memory or device emulation problem, so reasons are counted and ranked.
"""
import logging
from collections import Counter

LOG = logging.getLogger(__name__)


def tally(reasons):
    """Return a {reason: count} mapping preserving insertion order of input."""
    counts = Counter(str(r).strip().upper() for r in reasons or [] if r)
    return dict(counts)


def dominant_reason(counts):
    """Return the most frequent exit reason and its share of the total."""
    if not counts:
        return None, 0.0
    total = sum(counts.values())
    reason, top = max(counts.items(), key=lambda kv: kv[1])
    return reason, round(top / float(total), 3)


def suspicious(counts, reason='EPT_MISCONFIG', share=0.2):
    """Report whether one reason exceeds the share threshold."""
    total = sum((counts or {}).values())
    if total == 0:
        return False
    return counts.get(reason, 0) / float(total) >= share


__all__ = ['tally', 'dominant_reason', 'suspicious']
