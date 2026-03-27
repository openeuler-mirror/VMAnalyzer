#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VMAnalyzer gather module.

This module provides functions for gathering VM and host information.
All gather functions follow a consistent pattern:
    - Accept vm_name as the primary parameter
    - Return a dictionary with collected metrics
    - Handle errors gracefully and return None on failure

Example:
    >>> from gather import get_vm_cpu_utilization
    >>> result = get_vm_cpu_utilization("vm-01")
    >>> print(result)
    {'cpu_usage': 45.2, 'timestamp': '2024-03-27T10:00:00'}
"""

__version__ = "0.1.0"
__all__ = []
