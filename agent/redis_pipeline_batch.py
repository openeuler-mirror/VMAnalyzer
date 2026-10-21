"""Batch Redis writes into pipelines with a bounded buffer.

Sending one command per sample triples the round-trip overhead.  Grouping
writes into correctly typed pipelines improves throughput while capping the
buffer so a slow server cannot exhaust agent memory.
"""

import logging

LOG = logging.getLogger(__name__)


class PipelineBatcher:
    """Accumulate commands and flush them when a limit is reached."""

    def __init__(self, client, batch_size=200):
        if batch_size <= 0:
            raise ValueError("batch_size must be positive")
        self.client = client
        self.batch_size = batch_size
        self._buffer = []
        self.flushes = 0

    def add(self, operation, *args, **kwargs):
        """Queue one command, flushing automatically when the batch is full."""
        self._buffer.append((operation, args, kwargs))
        if len(self._buffer) >= self.batch_size:
            self.flush()

    def flush(self):
        """Execute queued commands in a single pipeline and clear the buffer."""
        if not self._buffer:
            return 0
        pipe = self.client.pipeline()
        for operation, args, kwargs in self._buffer:
            getattr(pipe, operation)(*args, **kwargs)
        pipe.execute()
        count = len(self._buffer)
        self._buffer = []
        self.flushes += 1
        LOG.debug("flushed %d command(s) in pipeline %d", count, self.flushes)
        return count

    def pending(self):
        """Return the number of commands waiting to be flushed."""
        return len(self._buffer)
