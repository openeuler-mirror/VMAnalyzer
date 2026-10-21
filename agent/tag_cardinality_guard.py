#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Cap label cardinality so exported metrics stay scrape-friendly."""

import logging

LOG = logging.getLogger(__name__)


class CardinalityGuard:
    """Remember accepted label values per tag until a cap is reached."""

    def __init__(self, limit=500):
        self.limit = int(limit)
        self._values = {}
        self.overflow = {}

    def admit(self, tag, value):
        """Return True when the value fits, otherwise count an overflow."""
        known = self._values.setdefault(tag, set())
        if value in known:
            return True
        if len(known) >= self.limit:
            self.overflow[tag] = self.overflow.get(tag, 0) + 1
            LOG.debug("tag %s overflowed at %s", tag, value)
            return False
        known.add(value)
        return True

    def cardinality(self, tag=None):
        """Accepted value count for one tag, or for every tag."""
        if tag is None:
            return sum(len(values) for values in self._values.values())
        return len(self._values.get(tag, ()))

    def report(self):
        """Summarise accepted and rejected values per tag."""
        return {
            tag: {
                "accepted": len(values),
                "rejected": self.overflow.get(tag, 0),
            }
            for tag, values in self._values.items()
        }
