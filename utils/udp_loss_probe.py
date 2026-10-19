"""UDP loss estimation from sequence gaps.

UDP has no retransmit, so loss is estimated from gaps in the sequence numbers
carried by the application payload.
"""
import logging

LOG = logging.getLogger(__name__)


def gaps(sequence_numbers):
    """Return the missing sequence numbers observed in the stream."""
    nums = sorted(int(n) for n in sequence_numbers or [])
    missing = []
    for a, b in zip(nums, nums[1:]):
        if b - a > 1:
            missing.extend(range(a + 1, b))
    return missing


def loss_ratio(sequence_numbers):
    """Return lost packets divided by total expected packets."""
    nums = sorted(int(n) for n in sequence_numbers or [])
    if len(nums) < 2:
        return 0.0
    expected = nums[-1] - nums[0] + 1
    lost = expected - len(nums)
    LOG.debug('udp lost %d/%d', lost, expected)
    return round(max(0, lost) / float(expected), 4)


__all__ = ['gaps', 'loss_ratio']
