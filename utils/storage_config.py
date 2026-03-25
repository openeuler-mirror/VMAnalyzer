#!/usr/bin/env python
# _*_coding: utf-8 _*_
"""存储后端配置"""
STORAGE_CONFIG = {
    "redis": {"host": "localhost", "port": 6379, "db": 0},
    "influxdb": {"host": "localhost", "port": 8086, "database": "vm_analyzer"},
    "prometheus": {"port": 9090}
}
