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
Configuration Validation Module for VMAnalyzer

This module provides configuration validation to ensure all settings
are correct before starting the application.
"""
import os
import re
import logging
from enum import Enum

try:
    import redis
    HAS_REDIS = True
except ImportError:
    HAS_REDIS = False

try:
    import libvirt
    HAS_LIBVIRT = True
except ImportError:
    HAS_LIBVIRT = False

logger = logging.getLogger(__name__)


class ValidationError(Enum):
    """Validation error types."""
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"


class ConfigValidator:
    """
    Validates VMAnalyzer configuration.
    """
    
    def __init__(self, config):
        """
        Args:
            config: Configuration dictionary or module
        """
        self.config = config
        self.errors = []
        self.warnings = []
    
    def validate_all(self):
        """
        Run all validation checks.
        
        Returns:
            tuple: (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []
        
        # Run validation checks
        self._validate_redis_config()
        self._validate_collection_config()
        self._validate_thresholds()
        self._validate_logging_config()
        self._validate_file_permissions()
        self._validate_dependencies()
        
        is_valid = len([e for e in self.errors if e['type'] == ValidationError.CRITICAL]) == 0
        
        return is_valid, self.errors, self.warnings
    
    def _validate_redis_config(self):
        """Validate Redis configuration."""
        redis_config = self._get_config('REDIS_DATABASE_CONFIG', {})
        
        # Check host
        host = redis_config.get('host', 'localhost')
        if not isinstance(host, str) or not host:
            self.errors.append({
                'type': ValidationError.CRITICAL,
                'field': 'redis.host',
                'message': 'Redis host must be a non-empty string'
            })
        
        # Check port
        port = redis_config.get('port', 6379)
        if not isinstance(port, int) or port < 1 or port > 65535:
            self.errors.append({
                'type': ValidationError.CRITICAL,
                'field': 'redis.port',
                'message': 'Redis port must be an integer between 1 and 65535'
            })
        
        # Check connection if redis module available
        if HAS_REDIS:
            try:
                r = redis.Redis(
                    host=host,
                    port=port,
                    socket_connect_timeout=2
                )
                r.ping()
            except redis.ConnectionError:
                self.errors.append({
                    'type': ValidationError.CRITICAL,
                    'field': 'redis.connection',
                    'message': f'Cannot connect to Redis at {host}:{port}'
                })
            except Exception as e:
                self.warnings.append({
                    'type': ValidationError.WARNING,
                    'field': 'redis.connection',
                    'message': f'Redis connection check failed: {e}'
                })
    
    def _validate_collection_config(self):
        """Validate collection configuration."""
        coll_config = self._get_config('VM_ANALYZERS_CONFIG', {})
        
        # Validate interval
        interval = coll_config.get('interval', 1)
        if not isinstance(interval, (int, float)) or interval < 0.1:
            self.errors.append({
                'type': ValidationError.CRITICAL,
                'field': 'collection.interval',
                'message': 'Collection interval must be at least 0.1 seconds'
            })
        elif interval < 1:
            self.warnings.append({
                'type': ValidationError.WARNING,
                'field': 'collection.interval',
                'message': 'Very short interval (< 1s) may cause high CPU usage'
            })
        
        # Validate duration
        duration = coll_config.get('duration', 10)
        if not isinstance(duration, int) or duration < 1:
            self.errors.append({
                'type': ValidationError.CRITICAL,
                'field': 'collection.duration',
                'message': 'Collection duration must be a positive integer'
            })
    
    def _validate_thresholds(self):
        """Validate alert thresholds."""
        thresholds = self._get_config('ALERT_THRESHOLDS', {})
        
        for key, value in thresholds.items():
            if 'usage' in key:
                if not isinstance(value, (int, float)) or value < 0 or value > 100:
                    self.errors.append({
                        'type': ValidationError.CRITICAL,
                        'field': f'thresholds.{key}',
                        'message': f'{key} must be a percentage between 0 and 100'
                    })
                elif value > 95:
                    self.warnings.append({
                        'type': ValidationError.WARNING,
                        'field': f'thresholds.{key}',
                        'message': f'{key} is very high (>95%), alerts may be too late'
                    })
                elif value < 50:
                    self.warnings.append({
                        'type': ValidationError.WARNING,
                        'field': f'thresholds.{key}',
                        'message': f'{key} is very low (<50%), may cause alert fatigue'
                    })
    
    def _validate_logging_config(self):
        """Validate logging configuration."""
        log_config = self._get_config('LOGGING_CONFIG', {})
        
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        level = log_config.get('level', 'INFO')
        
        if level not in valid_levels:
            self.errors.append({
                'type': ValidationError.WARNING,
                'field': 'logging.level',
                'message': f'Log level should be one of {valid_levels}'
            })
    
    def _validate_file_permissions(self):
        """Validate file and directory permissions."""
        # Check if config file is readable
        config_paths = [
            './config.py',
            '/etc/vmanalyzer/config.py'
        ]
        
        config_found = False
        for path in config_paths:
            if os.path.exists(path) and os.access(path, os.R_OK):
                config_found = True
                break
        
        if not config_found:
            self.warnings.append({
                'type': ValidationError.INFO,
                'field': 'config.file',
                'message': 'No readable config file found, using defaults'
            })
        
        # Check libvirt access
        libvirt_sockets = [
            '/run/libvirt/libvirt-sock',
            '/var/run/libvirt/libvirt-sock'
        ]
        
        socket_found = False
        for sock in libvirt_sockets:
            if os.path.exists(sock):
                socket_found = True
                if not os.access(sock, os.R_OK | os.W_OK):
                    self.errors.append({
                        'type': ValidationError.CRITICAL,
                        'field': 'libvirt.socket',
                        'message': f'Cannot access {sock}, check permissions'
                    })
                break
        
        if not socket_found:
            self.warnings.append({
                'type': ValidationError.WARNING,
                'field': 'libvirt.socket',
                'message': 'No libvirt socket found, libvirt may not be running'
            })
    
    def _validate_dependencies(self):
        """Validate required dependencies."""
        required_modules = {
            'libvirt': HAS_LIBVIRT,
            'redis': HAS_REDIS
        }
        
        for module, available in required_modules.items():
            if not available:
                self.errors.append({
                    'type': ValidationError.CRITICAL,
                    'field': f'dependencies.{module}',
                    'message': f'{module} Python module is not installed'
                })
    
    def _get_config(self, key, default=None):
        """Get configuration value."""
        if isinstance(self.config, dict):
            return self.config.get(key, default)
        else:
            return getattr(self.config, key, default)
    
    def print_report(self):
        """Print validation report."""
        print("\n" + "="*60)
        print("VMAnalyzer Configuration Validation Report")
        print("="*60)
        
        if not self.errors and not self.warnings:
            print("\n✓ All checks passed! Configuration is valid.")
            return
        
        if self.errors:
            print(f"\n✗ Found {len(self.errors)} error(s):")
            for error in self.errors:
                icon = "🔴" if error['type'] == ValidationError.CRITICAL else "🟡"
                print(f"  {icon} [{error['field']}] {error['message']}")
        
        if self.warnings:
            print(f"\n⚠ Found {len(self.warnings)} warning(s):")
            for warning in self.warnings:
                print(f"  🟡 [{warning['field']}] {warning['message']}")
        
        print("\n" + "="*60)


def validate_config_on_startup(config):
    """
    Validate configuration on application startup.
    Exits if critical errors are found.
    
    Args:
        config: Configuration module or dictionary
    """
    validator = ConfigValidator(config)
    is_valid, errors, warnings = validator.validate_all()
    
    # Log warnings
    for warning in warnings:
        logger.warning(f"Config warning [{warning['field']}]: {warning['message']}")
    
    # Log and exit on critical errors
    critical_errors = [e for e in errors if e['type'] == ValidationError.CRITICAL]
    if critical_errors:
        for error in critical_errors:
            logger.error(f"Config error [{error['field']}]: {error['message']}")
        logger.error("Configuration validation failed. Please fix the errors above.")
        raise SystemExit(1)
    
    # Log non-critical errors
    for error in errors:
        if error['type'] != ValidationError.CRITICAL:
            logger.warning(f"Config issue [{error['field']}]: {error['message']}")
    
    logger.info("Configuration validation passed")


# CLI interface
if __name__ == '__main__':
    import sys
    
    # Try to load config
    try:
        import config
        validator = ConfigValidator(config)
    except ImportError:
        print("Warning: Could not load config.py, using empty config")
        validator = ConfigValidator({})
    
    is_valid, errors, warnings = validator.validate_all()
    validator.print_report()
    
    sys.exit(0 if is_valid else 1)
