#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
"""Threshold checker that maps values to severity levels."""

OK = "ok"
WARN = "warn"
CRITICAL = "critical"


class ThresholdChecker(object):
    """Classify a value against configurable warn/critical thresholds."""

    def __init__(self, warn, critical, descending=False):
        if warn is None or critical is None:
            raise ValueError("warn and critical thresholds are required")
        self.warn = warn
        self.critical = critical
        self.descending = descending

    def check(self, value):
        """Return the severity level for the given value."""
        if value is None:
            return OK
        if self.descending:
            if value <= self.critical:
                return CRITICAL
            if value <= self.warn:
                return WARN
            return OK
        if value >= self.critical:
            return CRITICAL
        if value >= self.warn:
            return WARN
        return OK

    def is_critical(self, value):
        """Return True when the value reaches the critical threshold."""
        return self.check(value) == CRITICAL
