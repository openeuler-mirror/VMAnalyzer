"""
VMAnalyzer Configuration Example

Copy this file to config.py and modify according to your needs.
"""

# Redis connection settings
REDIS_HOST = "localhost"  # Redis server hostname
REDIS_PORT = 6379         # Redis server port
REDIS_DB = 0              # Redis database number

# Collection settings
COLLECTION_INTERVAL = 1   # Metrics collection interval in seconds
MAX_RETRIES = 3           # Maximum retry attempts for failed collections

# Alert thresholds (percentage)
ALERT_THRESHOLDS = {
    "cpu_warning": 70,    # CPU usage warning threshold
    "cpu_critical": 90,   # CPU usage critical threshold
    "memory_warning": 80, # Memory usage warning threshold
    "memory_critical": 95 # Memory usage critical threshold
}

# Logging configuration
LOG_LEVEL = "INFO"        # DEBUG, INFO, WARNING, ERROR
LOG_FILE = "/var/log/vm-analyzer.log"
