#!/usr/bin/env python
# _*_coding: utf-8 _*_
"""阈值配置模块"""
DEFAULT_THRESHOLDS = {
    "cpu_usage": 90.0,
    "memory_usage": 85.0,
    "disk_usage": 90.0,
    "network_drops": 100,
    "disk_io_wait": 50.0
}

# QEMU Guest Agent monitoring
ALERT_QEMU_AGENT_DOWN = True
