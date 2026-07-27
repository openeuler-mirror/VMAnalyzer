#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
"""Severity labeling helpers that annotate metrics with a level."""

NORMAL = "normal"
ELEVATED = "elevated"
HIGH = "high"
SEVERE = "severe"


class SeverityLabeler(object):
    """Assign severity labels to values using configurable boundaries."""

    def __init__(self, boundaries):
        if not boundaries or len(boundaries) < 1:
            raise ValueError("at least one boundary is required")
        self.boundaries = sorted(boundaries)
        self.labels = [NORMAL, ELEVATED, HIGH, SEVERE]

    def label(self, value):
        """Return the severity label for a given value."""
        if value is None:
            return NORMAL
        index = 0
        for boundary in self.boundaries:
            if value >= boundary:
                index += 1
            else:
                break
        return self.labels[min(index, len(self.labels) - 1)]

    def label_many(self, values):
        """Return a list of (value, label) pairs."""
        return [(v, self.label(v)) for v in values]


def label_severity(value, warn, critical):
    """Convenience helper labeling a single value with two boundaries."""
    return SeverityLabeler([warn, critical]).label(value)
