#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
"""Alert generation helpers for metric anomalies."""

INFO = "info"
WARNING = "warning"
ERROR = "error"


class Alert(object):
    """A single alert raised for a metric anomaly."""

    def __init__(self, level, name, message, value=None, threshold=None):
        self.level = level
        self.name = name
        self.message = message
        self.value = value
        self.threshold = threshold

    def to_dict(self):
        return {
            "level": self.level,
            "name": self.name,
            "message": self.message,
            "value": self.value,
            "threshold": self.threshold,
        }


class AlertRule(object):
    """A rule that raises an alert when value crosses a threshold."""

    def __init__(self, name, threshold, level=WARNING, message=None):
        self.name = name
        self.threshold = threshold
        self.level = level
        self.message = message or "%s exceeded threshold" % name

    def evaluate(self, value):
        if value is not None and value >= self.threshold:
            return Alert(self.level, self.name, self.message, value, self.threshold)
        return None


def generate_alerts(rules, values):
    """Evaluate a list of AlertRule against a dict of named values."""
    alerts = []
    for rule in rules:
        value = values.get(rule.name) if isinstance(values, dict) else None
        alert = rule.evaluate(value)
        if alert is not None:
            alerts.append(alert.to_dict())
    return alerts
