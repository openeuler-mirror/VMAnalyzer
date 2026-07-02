#!/usr/bin/env python
# _*_coding: utf-8 _*_
"""JSON格式日志工具"""

def get_json_formatter():
    """Get a JSON log formatter"""
    import json, logging
    
    class JsonFormatter(logging.Formatter):
        def format(self, record):
            log_entry = {
                "time": self.formatTime(record),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
            }
            if record.exc_info:
                log_entry["exception"] = self.formatException(record.exc_info)
            return json.dumps(log_entry, ensure_ascii=False)
    
    return JsonFormatter()
import json
import logging
class JSONFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage()
        })
