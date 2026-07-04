#!/usr/bin/env python
# _*_coding: utf-8 _*_
"""Documentation for this component."""
STORAGE_CONFIG = {
    "redis": {"host": "localhost", "port": 6379, "db": 0},
    "influxdb": {"host": "localhost", "port": 8086, "database": "vm_analyzer"},
    "prometheus": {"port": 9090}
}

# Multiple Redis instances support
REDIS_INSTANCES = [
    {
        "host": "localhost",
        "port": 6379,
        "db": 0,
        "role": "primary"
    }
    # Add additional Redis instances for high availability
    # {
    #     "host": "redis-2",
    #     "port": 6379,
    #     "db": 0,
    #     "role": "replica"
    # }
]
