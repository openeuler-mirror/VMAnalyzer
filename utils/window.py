#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
"""Sliding window container for streaming stat samples."""


class SlidingWindow(object):
    """A bounded FIFO window that keeps the most recent N samples."""

    def __init__(self, size):
        if size <= 0:
            raise ValueError("size must be positive")
        self.size = size
        self._items = []

    def push(self, item):
        """Add an item, evicting the oldest when full. Returns evicted item."""
        evicted = None
        if len(self._items) >= self.size:
            evicted = self._items.pop(0)
        self._items.append(item)
        return evicted

    def items(self):
        """Return a copy of the current window contents."""
        return list(self._items)

    def is_full(self):
        """Return True when the window has reached its capacity."""
        return len(self._items) >= self.size

    def clear(self):
        """Remove all items from the window."""
        self._items = []

    def __len__(self):
        return len(self._items)

    def average(self, value_key=None):
        """Return the average of numeric items (or item[value_key])."""
        if not self._items:
            return 0.0
        values = []
        for item in self._items:
            if isinstance(item, dict):
                v = item.get(value_key)
                if isinstance(v, (int, float)):
                    values.append(v)
            elif isinstance(item, (int, float)):
                values.append(item)
        if not values:
            return 0.0
        return sum(values) / len(values)
