#!/usr/bin/env python
# _*_coding: utf-8 _*_
"""告警管理系统"""
class AlertManager:
    def __init__(self):
        self.alerts = []
    def add_alert(self, level, message, source):
        self.alerts.append({"level": level, "message": message, "source": source})
    def get_alerts(self, level=None):
        if level:
            return [a for a in self.alerts if a["level"] == level]
        return self.alerts
