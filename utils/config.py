#!/usr/bin/env python
# _*_coding: utf-8 _*_
#######################################################################################
# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#          http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.
#######################################################################################
REDIS_DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 6379,
}

VM_ANALYZERS_CONFIG = {
    'duration': 10
}

# Alert thresholds: trigger a warning log when utilization exceeds these values.
# CPU/memory values are in percent (0–100).
ALERT_THRESHOLDS = {
    'cpu_usage': 90.0,
    'memory_usage': 85.0,
    'disk_write_bytes_rate': 0,
}

# Redis data retention: automatically remove stats entries older than this many
# seconds to prevent unbounded growth. Set to 0 to keep data forever.
REDIS_RETENTION_SECONDS = 3600  # 1 hour
import importlib
import os
import time

_config_modified_time = 0
_config = None

def reload_config():
    """Reload configuration file without restarting"""
    global _config_modified_time, _config
    
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.py')
    if not os.path.exists(config_path):
        return None
    
    mtime = os.path.getmtime(config_path)
    if mtime > _config_modified_time or _config is None:
        import config
        importlib.reload(config)
        _config = config
        _config_modified_time = mtime
        print("🔄 配置文件已重载")
    
    return _config
