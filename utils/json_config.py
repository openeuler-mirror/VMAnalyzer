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
"""
JSON Configuration Loader for VMAnalyzer

This module provides functionality to load configuration from JSON files,
providing an alternative to Python-based configuration.
"""
import json
import logging
import os
import logging

logger = logging.getLogger(__name__)

DEFAULT_CONFIG_PATHS = [
    '/etc/vmanalyzer/config.json',
    os.path.expanduser('~/.config/vmanalyzer/config.json'),
    './config.json',
    'config.json'
]


def load_json_config(path=None):
    """
    Load configuration from a JSON file.
    
    Args:
        path: Path to JSON config file. If None, searches default locations.
        
    Returns:
        dict: Configuration dictionary
        
    Raises:
        FileNotFoundError: If no config file found and path is None
        json.JSONDecodeError: If JSON is invalid
    """
    if path:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    for config_path in DEFAULT_CONFIG_PATHS:
        if os.path.exists(config_path):
            logger.info(f"Loading configuration from {config_path}")
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    
    raise FileNotFoundError("No configuration file found in default locations")


def merge_with_defaults(json_config):
    """
    Merge JSON configuration with default values.
    
    Args:
        json_config: Configuration loaded from JSON
        
    Returns:
        dict: Merged configuration
    """
    defaults = {
        'redis': {
            'host': 'localhost',
            'port': 6379,
            'db': 0,
            'password': None
        },
        'collection': {
            'interval': 1,
            'duration': 10,
            'timeout': None
        },
        'thresholds': {
            'cpu_usage': 90.0,
            'memory_usage': 85.0,
            'disk_usage': 90.0,
            'network_drops': 100
        },
        'retention': {
            'seconds': 3600
        },
        'logging': {
            'level': 'INFO',
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    }
    
    def deep_merge(base, override):
        """Deep merge two dictionaries."""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = deep_merge(result[key], value)
            else:
                result[key] = value
        return result
    
    return deep_merge(defaults, json_config)


def validate_config(config):
    """
    Validate configuration values.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        tuple: (is_valid, error_message)
    """
    errors = []
    
    # Validate Redis configuration
    if 'redis' in config:
        redis_config = config['redis']
        if 'port' in redis_config:
            port = redis_config['port']
            if not isinstance(port, int) or port < 1 or port > 65535:
                errors.append("Redis port must be an integer between 1 and 65535")
    
    # Validate collection interval
    if 'collection' in config:
        coll_config = config['collection']
        if 'interval' in coll_config:
            interval = coll_config['interval']
            if not isinstance(interval, (int, float)) or interval < 0.1:
                errors.append("Collection interval must be at least 0.1 seconds")
    
    # Validate thresholds
    if 'thresholds' in config:
        thresholds = config['thresholds']
        for key, value in thresholds.items():
            if 'usage' in key and (not isinstance(value, (int, float)) or value < 0 or value > 100):
                errors.append(f"{key} must be a percentage between 0 and 100")
    
    if errors:
        return False, "; ".join(errors)
    return True, None


class ConfigManager:
    """
    Configuration manager that supports both JSON and Python config files.
    """
    
    def __init__(self, config_path=None):
        self.config = {}
        self.config_path = config_path
        self._load_config()
    
    def _load_config(self):
        """Load configuration from available sources."""
        # Try JSON config first
        try:
            json_config = load_json_config(self.config_path)
            self.config = merge_with_defaults(json_config)
            is_valid, error = validate_config(self.config)
            if not is_valid:
                logger.warning(f"Configuration validation warning: {error}")
        except FileNotFoundError:
            logger.info("No JSON config found, using defaults")
            self.config = merge_with_defaults({})
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
            self.config = merge_with_defaults({})
    
    def get(self, key, default=None):
        """Get configuration value by key (supports dot notation)."""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def get_redis_config(self):
        """Get Redis configuration."""
        return self.config.get('redis', {})
    
    def get_collection_config(self):
        """Get collection configuration."""
        return self.config.get('collection', {})
    
    def get_thresholds(self):
        """Get alert thresholds."""
        return self.config.get('thresholds', {})
    
    def get_retention_seconds(self):
        """Get data retention time in seconds."""
        retention = self.config.get('retention', {})
        return retention.get('seconds', 3600)


# Example JSON config file format
EXAMPLE_CONFIG = """{
    "redis": {
        "host": "localhost",
        "port": 6379,
        "db": 0
    },
    "collection": {
        "interval": 1,
        "duration": 10
    },
    "thresholds": {
        "cpu_usage": 90.0,
        "memory_usage": 85.0,
        "disk_usage": 90.0
    },
    "retention": {
        "seconds": 3600
    },
    "logging": {
        "level": "INFO"
    }
}"""
