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
Health Check Module for VMAnalyzer

This module provides health check functionality to verify that all
components of VMAnalyzer are functioning correctly.
"""
import sys
import socket
import subprocess
import json
import logging
from datetime import datetime

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


class HealthChecker:
    """
    Health checker for VMAnalyzer components.
    """
    
    def __init__(self, redis_host='localhost', redis_port=6379, 
                 libvirt_uri='qemu:///system'):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.libvirt_uri = libvirt_uri
        self.checks = []
    
    def check_all(self):
        """
        Run all health checks.
        
        Returns:
            dict: Health check results
        """
        results = {
            'timestamp': datetime.now().isoformat(),
            'overall_status': 'healthy',
            'checks': {}
        }
        
        # Run individual checks
        checks_to_run = [
            ('redis', self.check_redis),
            ('libvirt', self.check_libvirt),
            ('disk_space', self.check_disk_space),
            ('memory', self.check_memory),
            ('permissions', self.check_permissions)
        ]
        
        for name, check_func in checks_to_run:
            try:
                check_result = check_func()
                results['checks'][name] = check_result
                if check_result['status'] != 'healthy':
                    results['overall_status'] = 'degraded'
            except Exception as e:
                results['checks'][name] = {
                    'status': 'unhealthy',
                    'error': str(e)
                }
                results['overall_status'] = 'unhealthy'
        
        return results
    
    def check_redis(self):
        """Check Redis connectivity."""
        if not HAS_REDIS:
            return {
                'status': 'unhealthy',
                'error': 'redis module not installed'
            }
        
        try:
            r = redis.Redis(
                host=self.redis_host,
                port=self.redis_port,
                socket_connect_timeout=5
            )
            r.ping()
            info = r.info()
            
            return {
                'status': 'healthy',
                'details': {
                    'version': info.get('redis_version'),
                    'connected_clients': info.get('connected_clients'),
                    'used_memory_human': info.get('used_memory_human'),
                    'uptime_in_days': info.get('uptime_in_days')
                }
            }
        except redis.ConnectionError as e:
            return {
                'status': 'unhealthy',
                'error': f'Cannot connect to Redis: {e}'
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e)
            }
    
    def check_libvirt(self):
        """Check libvirt connectivity."""
        if not HAS_LIBVIRT:
            return {
                'status': 'unhealthy',
                'error': 'libvirt module not installed'
            }
        
        try:
            conn = libvirt.open(self.libvirt_uri)
            if conn is None:
                return {
                    'status': 'unhealthy',
                    'error': 'Failed to open libvirt connection'
                }
            
            # Get basic info
            hostname = conn.getHostname()
            version = conn.getVersion()
            vm_count = len(conn.listAllDomains())
            
            conn.close()
            
            return {
                'status': 'healthy',
                'details': {
                    'hostname': hostname,
                    'version': version,
                    'vm_count': vm_count
                }
            }
        except libvirt.libvirtError as e:
            return {
                'status': 'unhealthy',
                'error': f'libvirt error: {e}'
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e)
            }
    
    def check_disk_space(self):
        """Check available disk space."""
        try:
            import shutil
            stat = shutil.disk_usage('/')
            
            total_gb = stat.total / (1024**3)
            free_gb = stat.free / (1024**3)
            used_percent = (stat.used / stat.total) * 100
            
            status = 'healthy'
            if used_percent > 90:
                status = 'unhealthy'
            elif used_percent > 80:
                status = 'degraded'
            
            return {
                'status': status,
                'details': {
                    'total_gb': round(total_gb, 2),
                    'free_gb': round(free_gb, 2),
                    'used_percent': round(used_percent, 2)
                }
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e)
            }
    
    def check_memory(self):
        """Check system memory."""
        try:
            with open('/proc/meminfo', 'r') as f:
                meminfo = f.read()
            
            mem_total = 0
            mem_available = 0
            
            for line in meminfo.split('\n'):
                if line.startswith('MemTotal:'):
                    mem_total = int(line.split()[1]) * 1024
                elif line.startswith('MemAvailable:'):
                    mem_available = int(line.split()[1]) * 1024
            
            if mem_total > 0:
                available_percent = (mem_available / mem_total) * 100
            else:
                available_percent = 0
            
            status = 'healthy'
            if available_percent < 5:
                status = 'unhealthy'
            elif available_percent < 10:
                status = 'degraded'
            
            return {
                'status': status,
                'details': {
                    'total_mb': round(mem_total / (1024**2), 2),
                    'available_mb': round(mem_available / (1024**2), 2),
                    'available_percent': round(available_percent, 2)
                }
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e)
            }
    
    def check_permissions(self):
        """Check if running with appropriate permissions."""
        import os
        
        checks = {
            'is_root': os.geteuid() == 0,
            'can_access_libvirt': False
        }
        
        # Try to access libvirt socket
        libvirt_sockets = [
            '/run/libvirt/libvirt-sock',
            '/var/run/libvirt/libvirt-sock'
        ]
        
        for sock in libvirt_sockets:
            if os.path.exists(sock) and os.access(sock, os.R_OK | os.W_OK):
                checks['can_access_libvirt'] = True
                break
        
        if checks['is_root'] or checks['can_access_libvirt']:
            return {
                'status': 'healthy',
                'details': checks
            }
        else:
            return {
                'status': 'degraded',
                'details': checks,
                'warning': 'Not running as root and cannot access libvirt socket'
            }


def print_health_report(results):
    """Print health report in human-readable format."""
    print("\n" + "="*60)
    print(f"VMAnalyzer Health Report")
    print(f"Timestamp: {results['timestamp']}")
    print("="*60)
    
    status_icon = {
        'healthy': '✓',
        'degraded': '⚠',
        'unhealthy': '✗'
    }
    
    overall = results['overall_status']
    print(f"\nOverall Status: {status_icon.get(overall, '?')} {overall.upper()}")
    print("-"*60)
    
    for check_name, check_result in results['checks'].items():
        status = check_result['status']
        icon = status_icon.get(status, '?')
        print(f"\n{icon} {check_name.upper()}")
        
        if 'details' in check_result:
            for key, value in check_result['details'].items():
                print(f"   {key}: {value}")
        
        if 'error' in check_result:
            print(f"   ERROR: {check_result['error']}")
        
        if 'warning' in check_result:
            print(f"   WARNING: {check_result['warning']}")
    
    print("\n" + "="*60)


def main():
    """Main entry point for health check script."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='VMAnalyzer Health Check Tool'
    )
    parser.add_argument(
        '--redis-host', default='localhost',
        help='Redis host (default: localhost)'
    )
    parser.add_argument(
        '--redis-port', type=int, default=6379,
        help='Redis port (default: 6379)'
    )
    parser.add_argument(
        '--libvirt-uri', default='qemu:///system',
        help='Libvirt URI (default: qemu:///system)'
    )
    parser.add_argument(
        '--json', action='store_true',
        help='Output as JSON'
    )
    
    args = parser.parse_args()
    
    checker = HealthChecker(
        redis_host=args.redis_host,
        redis_port=args.redis_port,
        libvirt_uri=args.libvirt_uri
    )
    
    results = checker.check_all()
    
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print_health_report(results)
    
    # Exit with appropriate code
    if results['overall_status'] == 'unhealthy':
        sys.exit(2)
    elif results['overall_status'] == 'degraded':
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
