#!/usr/bin/env python
# _*_coding: utf-8 _*_
"""告警管理系统"""
import logging

class AlertManager:
    """Manage and dispatch alerts."""
    def __init__(self):
        self.callbacks = []
        self.alert_history = []
    
    def register_callback(self, cb):
        self.callbacks.append(cb)
    
    def send_alert(self, alert):
        for cb in self.callbacks:
            try:
                cb(alert)
            except Exception as e:
                logging.error(f'Alert callback failed: {e}')
        self.alert_history.append(alert)
    
    def get_recent_alerts(self, count=10):
        return self.alert_history[-count:]
class AlertManager:
    def __init__(self):
        self._recent = {}
        self.alerts = []
    def add_alert(self, level, message, source):
        self.alerts.append({"level": level, "message": message, "source": source})
    def get_alerts(self, level=None):
        if level:
            return [a for a in self.alerts if a["level"] == level]
        return self.alerts
