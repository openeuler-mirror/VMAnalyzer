#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Resolve legacy metric names to their canonical namespace."""

import logging

LOG = logging.getLogger(__name__)

DEFAULT_ALIASES = {
    "cpu.usage": "vm.cpu.utilization",
    "cpu.steal": "vm.cpu.steal_time",
    "mem.used": "vm.memory.used",
    "net.rx": "vm.network.rx_bytes",
    "net.tx": "vm.network.tx_bytes",
}


class NamespaceResolver:
    """Apply alias rules and remember unknown names."""

    def __init__(self, aliases=None):
        self.aliases = dict(DEFAULT_ALIASES)
        if aliases:
            self.aliases.update(aliases)
        self.unknown = set()

    def resolve(self, name):
        """Return the canonical name for *name*."""
        canonical = self.aliases.get(name)
        if canonical is not None:
            return canonical
        if name not in self.aliases.values():
            self.unknown.add(name)
            LOG.debug("unmapped metric name %s", name)
        return name

    def map_all(self, names):
        """Resolve a sequence of names while preserving order."""
        return [self.resolve(name) for name in names]

    def add(self, legacy, canonical):
        """Register an additional alias at runtime."""
        self.aliases[legacy] = canonical


def canonical(name, aliases=None):
    """Convenience one-shot resolver."""
    return NamespaceResolver(aliases).resolve(name)
