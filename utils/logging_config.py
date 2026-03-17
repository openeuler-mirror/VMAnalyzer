#!/usr/bin/env python
# _*_coding: utf-8 _*_
"""日志配置模块"""
LOGGING_CONFIG = {
    "version": 1,
    "formatters": {
        "standard": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"},
        "json": {"format": "%(message)s"}
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "standard"},
        "file": {"class": "logging.FileHandler", "filename": "vm_analyzer.log", "formatter": "standard"}
    },
    "loggers": {
        "vm_analyzer": {"handlers": ["console", "file"], "level": "INFO"}
    }
}
