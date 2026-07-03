#!/usr/bin/env python
# _*_coding: utf-8 _*_
"""告警级别常量"""

CRITICAL = "critical"
WARNING = "warning"
INFO = "info"

def validate_level(level):
    """Check if level is valid"""
    return level in (CRITICAL, WARNING, INFO)
ALERT_LEVEL_INFO = "info"
ALERT_LEVEL_WARNING = "warning"
ALERT_LEVEL_ERROR = "error"
ALERT_LEVEL_CRITICAL = "critical"
ALERT_LEVELS = [ALERT_LEVEL_INFO, ALERT_LEVEL_WARNING, ALERT_LEVEL_ERROR, ALERT_LEVEL_CRITICAL]
