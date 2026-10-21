#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Rolling window statistics for a single metric series."""

import logging
from collections import deque

LOG = logging.getLogger(__name__)


class RollingWindow:
    """Keep the most recent *size* values and expose summary statistics."""

    def __init__(self, size=30):
        if size <= 0:
            raise ValueError("size must be positive")
        self.size = int(size)
        self.values = deque(maxlen=self.size)

    def add(self, value):
        """Append a value and return the updated mean."""
        self.values.append(float(value))
        return self.mean()

    def mean(self):
        """Arithmetic mean of the retained values."""
        if not self.values:
            return 0.0
        return sum(self.values) / len(self.values)

    def maximum(self):
        """Largest retained value, or zero when empty."""
        return max(self.values) if self.values else 0.0

    def minimum(self):
        """Smallest retained value, or zero when empty."""
        return min(self.values) if self.values else 0.0

    def spread(self):
        """Difference between the newest and oldest retained values."""
        if len(self.values) < 2:
            return 0.0
        return self.values[-1] - self.values[0]
