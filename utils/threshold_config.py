#!/usr/bin/env python
# _*_coding: utf-8 _*_
"""Documentation for this component."""
DEFAULT_THRESHOLDS = {
    "cpu_usage": 90.0,
    "memory_usage": 85.0,
    "disk_usage": 90.0,
    "network_drops": 100,
    "disk_io_wait": 50.0
}

# QEMU Guest Agent monitoring
ALERT_QEMU_AGENT_DOWN = True

# Network packet loss thresholds
NETWORK_PACKET_LOSS_WARNING = 1.0  # 1%
NETWORK_PACKET_LOSS_CRITICAL = 5.0 # 5%
