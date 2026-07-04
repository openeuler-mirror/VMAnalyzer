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
        LOG_INFO(f"\n===== 开始处理VM：{vm_name} =====")
        dom = conn.lookupByName(vm_name)
        if not dom:
            LOG_ERROR(f"未找到名称为 {vm_name} 的VM")
            return vm_stats
        
        vm["uuid"] = dom.UUIDString()
        vm_id = vm["uuid"]
        vm_state = dom.state()[0]
        state_map = {
            libvirt.VIR_DOMAIN_RUNNING: "running",
            libvirt.VIR_DOMAIN_SHUTOFF: "shutoff",
            libvirt.VIR_DOMAIN_PAUSED: "paused"
        }
        vm_status = state_map.get(vm_state, f"unknown state({vm_state})")
        LOG_INFO(f"VM信息：名称={vm_name}, UUID={vm_id}, 状态={vm_status}")
        
        LOG_INFO(f"正在Parse {vm_name} 的 XML 配置...")
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
        
        vcpupin_stats = {}
        for vcpu_id in range(vcpu_total):
            LOG_INFO(f"{vm_name} - 正在获取 vCPU {vcpu_id} 的亲和性信息...")
            pin_info = {}
            try:
                result = subprocess.run(
                    ['virsh', 'vcpupin', vm_name, str(vcpu_id)],
                    capture_output=True,
                    text=True,
                    check=True,
                    timeout=10
                )
                
                output = result.stdout.strip()
                affinity_str = extract_affinity_from_output(output, vcpu_id)
                if not affinity_str:
                    raise Exception(f"未从输出中找到亲和性信息")
                
                allowed_physical_cpus = parse_affinity_string(affinity_str)
                pin_info['vcpu_id'] = vcpu_id
                pin_info['affinity_mask_hex'] = 'N/A'
                pin_info['mask_length_bytes'] = 0
                pin_info['allowed_physical_cpus'] = allowed_physical_cpus
                pin_info['physical_cpu_count'] = len(allowed_physical_cpus)
                pin_info['affinity_string'] = affinity_str
                pin_info['socket'] = socket
                pin_info['core'] = core
                pin_info['thread'] = thread
                pin_info['status'] = 'success'
                
                LOG_INFO(f"{vm_name} - vCPU {vcpu_id} 亲和性信息获取成功：绑定物理CPU范围={allowed_physical_cpus}")
            
            except subprocess.CalledProcessError as e:
                error_msg = f"Command failed：{e.stderr.strip()}"
                LOG_ERROR(f"{vm_name} - 获取 vCPU {vcpu_id} 亲和性信息失败：{error_msg}")
                pin_info = {
                    'vcpu_id': vcpu_id,
                    'status': 'failed',
                    'error_msg': error_msg,
                    'allowed_physical_cpus': [],
                    'physical_cpu_count': 0,
                    'affinity_string': '',
                    'socket': socket,
                    'core': core,
                    'thread': thread,
                    'affinity_mask_hex': 'N/A',
                    'mask_length_bytes': 0
                }
            except subprocess.TimeoutExpired:
                error_msg = "Operation message"
                LOG_ERROR(f"{vm_name} - 获取 vCPU {vcpu_id} 亲和性信息失败：{error_msg}")
                pin_info = {
                    'vcpu_id': vcpu_id,
                    'status': 'failed',
                    'error_msg': error_msg,
                    'allowed_physical_cpus': [],
                    'physical_cpu_count': 0,
                    'affinity_string': '',
                    'socket': socket,
                    'core': core,
                    'thread': thread,
                    'affinity_mask_hex': 'N/A',
                    'mask_length_bytes': 0
                }
            except Exception as e:
                error_msg = str(e)
                LOG_ERROR(f"{vm_name} - 获取 vCPU {vcpu_id} 亲和性信息失败：{error_msg}")
                pin_info = {
                    'vcpu_id': vcpu_id,
                    'status': 'failed',
                    'error_msg': error_msg,
                    'allowed_physical_cpus': [],
                    'physical_cpu_count': 0,
                    'affinity_string': '',
                    'socket': socket,
                    'core': core,
                    'thread': thread,
                    'affinity_mask_hex': 'N/A',
                    'mask_length_bytes': 0
                }
            
            vcpupin_stats[f'vcpu_{vcpu_id}'] = pin_info
        
        vm_stats[vm_id] = {
            'uuid': vm['uuid'],
            'name': vm['name'],
            'status': vm_status,
            'vcpu_total': vcpu_total,
            'vcpu_topology': {
                'socket': socket,
                'core': core,
                'thread': thread
            },
            'vcpupin_stats': vcpupin_stats,
            'timestamp': int(time.time())
        }
        
        context.xpathFreeContext()
        doc.freeDoc()
        LOG_INFO(f"{vm_name} - XML 资源已释放")
    
    except libvirt.libvirtError as e:
        LOG_ERROR(f"{vm_name} - 处理VM失败：{str(e)}")
    finally:
        if dom:
            dom = None
    
    return vm_stats

def get_all_vms_vcpupin() -> dict:
    """Documentation for this component."""
    conn = None
    all_vms_stats = {}
    
    try:
        LOG_INFO("Operation message")
        conn = libvirt.open("qemu:///system")
        if not conn:
            LOG_ERROR("Operation message")
            return all_vms_stats
        
        LOG_INFO("Operation message")
        domains = conn.listAllDomains()
        vm_names = [dom.name() for dom in domains]
        
        if not vm_names:
            LOG_INFO("No virtual machines found")
            return all_vms_stats
        
        LOG_INFO(f"Found {len(vm_names)} virtual machines：{vm_names}")
        
        for vm_name in vm_names:
            single_vm_stats = get_single_vm_vcpupin(vm_name, conn)
            all_vms_stats.update(single_vm_stats)
    
    except libvirt.libvirtError as e:
        LOG_ERROR(f"程序执行异常：{str(e)}")
    finally:
        if conn:
            conn.close()
            LOG_INFO("Operation message")
    
    return all_vms_stats

def main():
    if len(sys.argv) != 1:
        print("Usage: python3 vcpupin_check_all.py")
        print("Operation message")
        sys.exit(1)
    
    LOG_INFO("Operation message")
    all_stats = get_all_vms_vcpupin()
    
    if all_stats:
        LOG_INFO(f"\n===== 所有VM vCPU 绑核检测完成，共处理 {len(all_stats)} virtual machines =====")
        filename = f"vcpupin_stats_all_vms_{int(time.time())}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(all_stats, f, indent=2, ensure_ascii=False)
        LOG_INFO(f"结果已保存到文件：{filename}")
        
        print("Operation message")
        for vm_uuid, vm_info in all_stats.items():
            print(f"VM：{vm_info['name']}（{vm_info['status']}）- vCPU总数：{vm_info['vcpu_total']}")
    else:
        LOG_ERROR("Operation message")
        sys.exit(1)

if __name__ == "__main__":
    main()
