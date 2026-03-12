#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VMAnalyzer配置示例文件
复制此文件为config.py并根据实际情况修改配置
"""
# Redis数据库配置
REDIS_DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    'password': None,
    'socket_timeout': 5,
    'socket_connect_timeout': 5,
}
# 分析器配置
VM_ANALYZERS_CONFIG = {
    'duration': 10,  # 报告间隔，单位秒
}
# 告警阈值配置
ALERT_THRESHOLDS = {
    'cpu_usage': 90.0,  # CPU使用率告警阈值，百分比
    'memory_usage': 85.0,  # 内存使用率告警阈值，百分比
    'disk_usage': 90.0,  # 磁盘使用率告警阈值，百分比
    'network_bandwidth_usage': 80.0,  # 网络带宽使用率告警阈值，百分比
}
# Redis数据保留时间
REDIS_RETENTION_SECONDS = 3600  # 数据保留1小时
# 采集间隔
COLLECTION_INTERVAL = 1  # 指标采集间隔，单位秒
# Libvirt连接URI
LIBVIRT_URI = 'qemu:///system'
# 日志配置
LOG_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': '/var/log/vm_analyzer.log',
    'max_file_size': 10485760,  # 10MB
    'backup_count': 5,
}
