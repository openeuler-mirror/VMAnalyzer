#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import json
from lxml import etree
from typing import Optional, Dict, Any
import os
import re

def execute_cmd(cmd: list, timeout: int = 30) -> Dict[str, Any]:
    """
    执行系统命令，返回标准化结果
    :param cmd: 命令列表（如 ["virsh", "domstate", "vm1"]）
    :param timeout: 超时时间
    :return: {"code": 0/非0, "stdout": 输出内容, "stderr": 错误内容}
    """
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

"""采集虚机虚拟网卡类型及配置"""
def get_vm_nic_list(vm_name: str) -> list:
    nics = []
    cmd = ["virsh", "domiflist", vm_name]
    cmd_result = execute_cmd(cmd)
    if cmd_result["code"] != 0:
        return nics

    # 解析domiflist输出（跳过表头）
    lines = cmd_result["stdout"].split("\n")[2:]
    for line in lines:
        line = line.strip()
        if not line or line.startswith("---"):
            continue
        parts = re.split(r"\s+", line)
        if len(parts) >= 4:
            nics.append({
                "interface": parts[0],
                "type": parts[1],
                "source": parts[2],
                "model": parts[3],
            })
    return nics

def get_vm_network_vnic_type(vm_name: str) -> str:
    result = {
        "vm_name": vm_name,
        "nics": [],
        "success": False,
        "error": ""
    }

    # 获取网卡列表
    nics = get_vm_nic_list(vm_name)
    if not nics:
        result["error"] = "未获取到虚机网卡列表"
        return json.dumps(result, ensure_ascii=False, indent=2)

    # 整理网卡信息
    for nic in nics:
        nic_info = {
            "nic_name": nic["interface"],
            "type": nic["type"],
            "host_iface": nic["source"],
        }
        result["nics"].append(nic_info)

    result["success"] = True
    return json.dumps(result, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python get_vm_network_vnic_type.py <vm-name>")
        sys.exit(1)
    print(get_vm_network_vnic_type(sys.argv[1]))
