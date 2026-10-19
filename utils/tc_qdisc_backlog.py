"""Traffic control qdisc backlog parsing.

Persistent backlog in a qdisc means the shaped rate is below the offered
load; backlog samples are folded into a per qdisc summary.
"""
import logging

LOG = logging.getLogger(__name__)


def parse_qdisc_line(line):
    """Extract (qdisc_name, backlog_packets) from a tc -s line, or None."""
    parts = str(line or '').split()
    if 'qdisc' not in parts or 'backlog' not in parts:
        return None
    try:
        name = parts[parts.index('qdisc') + 1]
        backlog = parts[parts.index('backlog') + 1]
        packets = int(backlog.rstrip('p'))
        return name, packets
    except (ValueError, IndexError):
        return None


def hottest_qdisc(samples):
    """Return the qdisc name with the highest mean backlog."""
    per = {}
    for name, packets in samples or []:
        per.setdefault(name, []).append(int(packets))
    if not per:
        return None
    best = max(per.items(), key=lambda kv: sum(kv[1]) / len(kv[1]))
    LOG.debug('hottest qdisc %s', best[0])
    return best[0]


__all__ = ['parse_qdisc_line', 'hottest_qdisc']
