#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Session epoch markers so stale collectors can detect a restart."""

import logging
import os
import time

LOG = logging.getLogger(__name__)


def new_epoch():
    """Return a sortable epoch string for a fresh collector session."""
    stamp = time.strftime("%Y%m%dT%H%M%S", time.gmtime())
    return "{}-{}".format(stamp, os.getpid())


def is_stale(sample_epoch, current_epoch):
    """True when a sample predates the running session."""
    if not sample_epoch:
        return True
    return sample_epoch != current_epoch


class EpochTracker:
    """Own the epoch and count rejected stale samples."""

    def __init__(self, epoch=None):
        self.epoch = epoch or new_epoch()
        self.rejected = 0

    def accept(self, sample_epoch):
        """Accept a sample only when it belongs to the current epoch."""
        if is_stale(sample_epoch, self.epoch):
            self.rejected += 1
            LOG.debug("dropped sample from epoch %s", sample_epoch)
            return False
        return True

    def rotate(self):
        """Start a new epoch and return its identifier."""
        self.epoch = new_epoch()
        LOG.info("rotated collection epoch to %s", self.epoch)
        return self.epoch
