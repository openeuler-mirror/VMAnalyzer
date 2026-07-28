#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
"""Fixed-size ring buffer for keeping a bounded history of samples."""


class RingBuffer(object):
    """A circular buffer that overwrites the oldest entries when full."""

    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._buffer = [None] * capacity
        self._head = 0
        self._count = 0

    def append(self, item):
        """Add an item, overwriting the oldest when at capacity."""
        self._buffer[self._head] = item
        self._head = (self._head + 1) % self.capacity
        if self._count < self.capacity:
            self._count += 1

    def to_list(self):
        """Return the buffer contents in insertion order."""
        if self._count < self.capacity:
            return list(self._buffer[:self._count])
        return list(self._buffer[self._head:] + self._buffer[:self._head])

    def __len__(self):
        return self._count

    def is_full(self):
        return self._count == self.capacity

    def latest(self):
        """Return the most recently appended item, or None if empty."""
        if self._count == 0:
            return None
        index = (self._head - 1) % self.capacity
        return self._buffer[index]
