"""Retry policy for pipeline retry requests that fail transiently.

Hypervisor calls fail for reasons that disappear on their own, but retrying
without a deadline turns a slow path into a hang.  The policy bounds both the
attempt count and the total elapsed time.
"""

import logging
import time

LOG = logging.getLogger(__name__)


class PipelineRetryRetryPolicy:
    """Bounded retry loop with linear backoff and a hard deadline."""

    def __init__(self, attempts=3, delay=0.5, deadline=10.0):
        self.attempts = max(1, int(attempts))
        self.delay = max(0.0, float(delay))
        self.deadline = max(0.0, float(deadline))

    def run(self, call, *args, **kwargs):
        """Call *call* until it succeeds, attempts run out or time expires."""
        started = time.time()
        last_error = None
        for attempt in range(1, self.attempts + 1):
            try:
                return call(*args, **kwargs)
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                if time.time() - started >= self.deadline:
                    LOG.warning("pipeline_retry deadline reached after %d tries", attempt)
                    break
                LOG.info("pipeline_retry attempt %d failed: %s", attempt, exc)
                time.sleep(self.delay * attempt)
        raise last_error


__all__ = ["PipelineRetryRetryPolicy"]
