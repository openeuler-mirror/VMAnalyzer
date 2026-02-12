#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import libvirt
import libxml2
import json
import logging
import sys
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
LOG_INFO = logging.info
LOG_ERROR = logging.error

def parse_affinity_string(affinity_str: str) -> list:
    allowed_cpus = []
    affinity_str = affinity_str.strip().lower()
    
    if not affinity_str or affinity_str == 'all':
        return allowed_cpus
    elif '-' in affinity_str:
        try:
            start, end = map(int, affinity_str.split('-'))
            if start <= end:
                allowed_cpus = list(range(start, end + 1))
        except ValueError:
            LOG_ERROR(f"无效的亲和性范围格式：{affinity_str}")
    elif ',' in affinity_str:
        try:
            allowed_cpus = list(map(int, affinity_str.split(',')))
        except ValueError:
            LOG_ERROR(f"无效的亲和性列表格式：{affinity_str}")
    elif affinity_str.isdigit():
        allowed_cpus = [int(affinity_str)]
    else:
        LOG_ERROR(f"不支持的亲和性格式：{affinity_str}")
    
    return allowed_cpus

def extract_affinity_from_output(output: str, vcpu_id: int) -> str:
    output_lines = [line.strip() for line in output.split('\n') if line.strip()]
    target_vcpu_str = str(vcpu_id)
    
    for line in output_lines:
        if 'CPU Affinity:' in line:
            affinity_part = line.split('CPU Affinity:')[-1].strip()
            if affinity_part:
                return affinity_part
    
    return ""


if __name__ == "__main__":
    main()
