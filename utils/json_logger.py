#!/usr/bin/env python
# _*_coding: utf-8 _*_
"""JSON格式日志工具"""
import json
import logging
class JSONFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage()
        })
