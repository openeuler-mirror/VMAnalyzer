"""SCSI sense error accounting.

Medium errors outrank transport errors because they predict media failure, so
sense counters are weighted into a single risk score.
"""
import logging

LOG = logging.getLogger(__name__)


def risk_score(medium, transport, hardware):
    """Return a weighted risk score from SCSI sense counters."""
    score = 3 * int(medium or 0) + 2 * int(hardware or 0) + int(transport or 0)
    LOG.debug('scsi risk score %d', score)
    return score


def replace_advised(score, threshold=50):
    """Report when the risk score advises device replacement."""
    return int(score or 0) >= threshold


__all__ = ['risk_score', 'replace_advised']
