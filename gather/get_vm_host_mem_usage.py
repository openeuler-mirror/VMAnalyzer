#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import json
from lxml import etree
from typing import Optional, Dict, Any
import os
import re
import sys

def execute_cmd(cmd: list, timeout: int = 30) -> Dict[str, Any]:
    result = {
        "code": -1,
        "stdout": "",
        "stderr": ""
    }
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout
        )
        result["code"] = proc.returncode
        result["stdout"] = proc.stdout.strip()
        result["stderr"] = proc.stderr.strip()
    except subprocess.TimeoutExpired:
        result["stderr"] = f"命令执行超时（{timeout}s）: {' '.join(cmd)}"
    except Exception as e:
        result["stderr"] = f"命令执行异常: {str(e)}"
    return result

def get_vm_pid(vm_name: str) -> str:
    cmd = ["ps", "-ef"]
    ps_result = execute_cmd(cmd)
    if ps_result["code"] != 0:
        return ""
    qemu_pattern = re.compile(rf"guest={vm_name}", re.I)
    for line in ps_result["stdout"].split("\n"):
        if qemu_pattern.search(line):
            parts = line.split()
            return parts[1] if len(parts) >= 2 else ""
    return ""

def get_vm_list() -> list:
    """获取宿主机所有虚机名称列表"""
    cmd_result = execute_cmd(["virsh", "list", "--all", "--name"])
    if cmd_result["code"] != 0:
        return []
    return [vm for vm in cmd_result["stdout"].split("\n") if vm.strip()]

"""采集虚机占用宿主机内存（RSS/VSZ）"""
def get_vm_host_mem_usage(vm_name: str) -> str:
    """
    获取虚机进程占用的物理内存（RSS）和虚拟内存（VSZ）
    单位：MB
    """
    result = {
        "vm_name": vm_name,
        "pid": "",
        "rss_mb": 0.0,  # 物理内存
        "vsz_mb": 0.0,  # 虚拟内存
        "mem_percent": 0.0,  # 占宿主机总内存百分比
        "success": False,
        "error": ""
    }

    # 1. 获取PID
    pid_str = get_vm_pid(vm_name)
    if not pid_str or not pid_str.isdigit():
        result["error"] = "未找到虚机对应的QEMU进程"
        return json.dumps(result, ensure_ascii=False, indent=2)
    result["pid"] = pid_str
    pid = int(pid_str)

    # 2. 获取内存使用
    try:
        proc = psutil.Process(pid)
        mem_info = proc.memory_info()
        # 转换为MB（1MB=1024*1024字节）
        result["rss_mb"] = round(mem_info.rss / (1024 * 1024), 2)
        result["vsz_mb"] = round(mem_info.vms / (1024 * 1024), 2)
        # 计算占宿主机总内存百分比
        total_mem = psutil.virtual_memory().total / (1024 * 1024)
        result["mem_percent"] = round(result["rss_mb"] / total_mem * 100, 2)
        result["success"] = True
    except psutil.NoSuchProcess:
        result["error"] = "QEMU进程已退出"
    except Exception as e:
        result["error"] = f"获取内存信息失败: {str(e)}"

    return json.dumps(result, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    vms = get_vm_list()
    if not vms:
        print(json.dumps({"error": "没有找到任何虚机或执行virsh命令失败"}, ensure_ascii=False, indent=2))
        sys.exit(1)

    results = []
    for vm in vms:
        vm_result_json = get_vm_host_mem_usage(vm)
        vm_result = json.loads(vm_result_json)
        results.append(vm_result)

    # 输出所有虚机的结果（JSON数组）
    print(json.dumps(results, ensure_ascii=False, indent=2))
