#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
"""Clamp helpers that keep values within a safe bounded range."""


def clamp(value, low, high):
    """Restrict value to the [low, high] range."""
    if value is None:
        return low
    if value < low:
        return low
    if value > high:
        return high
    return value


def clamp_series(values, low, high):
    """Return a new list with every value clamped to [low, high]."""
    return [clamp(v, low, high) for v in values]


def clamp_percent(value):
    """Clamp a ratio-like value into the 0..100 percentage range."""
    return clamp(value, 0, 100)


class BoundedValue(object):
    """A mutable holder that always keeps its value within bounds."""

    def __init__(self, initial, low, high):
        self.low = low
        self.high = high
        self._value = clamp(initial, low, high)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = clamp(new_value, self.low, self.high)

    def is_at_limit(self):
        return self._value == self.low or self._value == self.high
