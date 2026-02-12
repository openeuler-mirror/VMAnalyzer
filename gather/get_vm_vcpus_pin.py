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
    
    for line in output_lines:
        if 'VCPU' in line and 'CPU Affinity' in line:
            continue
        parts = line.split()
        if len(parts) >= 2:
            parsed_vcpu_id = parts[0].strip()
            if parsed_vcpu_id == target_vcpu_str:
                return parts[1].strip()
    
    if len(output_lines) == 1:
        line = output_lines[0].strip()
        if any(char in line for char in '- ,') or line.isdigit():
            return line
    
    return ""

def get_single_vm_vcpupin(vm_name: str, conn: libvirt.virConnect) -> dict:
    dom = None
    vm_stats = {}
    vm = {"uuid": "", "name": vm_name}
    
    try:
        LOG_INFO(f"\n===== 开始处理虚拟机：{vm_name} =====")
        dom = conn.lookupByName(vm_name)
        if not dom:
            LOG_ERROR(f"未找到名称为 {vm_name} 的虚拟机")
            return vm_stats
        
        vm["uuid"] = dom.UUIDString()
        vm_id = vm["uuid"]
        vm_state = dom.state()[0]
        state_map = {
            libvirt.VIR_DOMAIN_RUNNING: "运行中",
            libvirt.VIR_DOMAIN_SHUTOFF: "已关闭",
            libvirt.VIR_DOMAIN_PAUSED: "已暂停"
        }
        vm_status = state_map.get(vm_state, f"未知状态({vm_state})")
        LOG_INFO(f"虚拟机信息：名称={vm_name}, UUID={vm_id}, 状态={vm_status}")
        
        LOG_INFO(f"正在解析 {vm_name} 的 XML 配置...")
        xmldesc = dom.XMLDesc(0)
        doc = libxml2.parseDoc(xmldesc)
        context = doc.xpathNewContext()
        
        vcpu_total = 0
        res = context.xpathEval('/domain/vcpu')
        if res and len(res) > 0:
            vcpu_total = int(res[0].content)
        LOG_INFO(f"{vm_name} - vCPU 总数：{vcpu_total}")
        
        topology = context.xpathEval('/domain/cpu/topology')
        socket = 0
        core = 0
        thread = 0
        if topology and len(topology) > 0:
            socket = int(topology[0].prop('sockets')) if topology[0].prop('sockets') else 0
            core = int(topology[0].prop('cores')) if topology[0].prop('cores') else 0
            thread = int(topology[0].prop('threads')) if topology[0].prop('threads') else 0
        LOG_INFO(f"{vm_name} - vCPU 拓扑：socket={socket}, core={core}, thread={thread}")
        
    
    return vm_stats


if __name__ == "__main__":
    main()
