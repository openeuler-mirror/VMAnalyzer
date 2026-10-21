#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Token bucket limiting how many retries a VM may spend per window."""

import logging
import time

LOG = logging.getLogger(__name__)


class RetryBudget:
    """Refill retry tokens at a fixed rate per VM."""

    def __init__(self, capacity=3, refill_per_second=0.2, clock=time.monotonic):
        self.capacity = float(capacity)
        self.refill = float(refill_per_second)
        self.clock = clock
        self._tokens = {}
        self._stamps = {}

    def _top_up(self, vm_name, now):
        last = self._stamps.get(vm_name, now)
        tokens = self._tokens.get(vm_name, self.capacity)
        tokens = min(self.capacity, tokens + (now - last) * self.refill)
        self._tokens[vm_name] = tokens
        self._stamps[vm_name] = now
        return tokens

    def try_consume(self, vm_name):
        """Spend one token when available, otherwise refuse the retry."""
        now = self.clock()
        tokens = self._top_up(vm_name, now)
        if tokens < 1.0:
            LOG.debug("retry budget exhausted for %s", vm_name)
            return False
        self._tokens[vm_name] = tokens - 1.0
        return True

    def available(self, vm_name):
        """Current token count without spending one."""
        return self._top_up(vm_name, self.clock())

    def reset(self, vm_name=None):
        """Restore full budget for one VM or for all VMs."""
        if vm_name is None:
            self._tokens.clear()
            self._stamps.clear()
        else:
            self._tokens.pop(vm_name, None)
            self._stamps.pop(vm_name, None)
