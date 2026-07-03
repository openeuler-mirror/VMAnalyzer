#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import json
from lxml import etree
from typing import Dict, Any
import os
import re

def execute_cmd(cmd: list, timeout: int = 30) -> Dict[str, Any]:
    """
    执行系统命令，返回标准化结果
    :param cmd: 命令列表（如 ["virsh", "domstate", "vm1"]）
    :param timeout: 超时时间
    :return: {"code": 0/非0, "stdout": 输出内容, "stderr": Error内容}
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
        result["stderr"] = f"Command timed out（{timeout}s）: {' '.join(cmd)}"
    except Exception as e:
        result["stderr"] = f"Command raised an exception: {str(e)}"
    return result

def get_vm_list() -> list:
    """获取host所有虚机名称列表"""
    cmd_result = execute_cmd(["virsh", "list", "--all", "--name"])
    if cmd_result["code"] != 0:
        return []
    return [vm for vm in cmd_result["stdout"].split("\n") if vm.strip()]

def get_vm_disk_list(vm_name: str) -> list:
    """获取虚机disk列表"""
    disks = []
    cmd = ["virsh", "domblklist", vm_name, "--details"]
    cmd_result = execute_cmd(cmd)
    if cmd_result["code"] != 0:
        return disks,f"执行virsh domblklist失败: {cmd_result['stderr']}"

    # Parsedomblklist输出（跳过表头）
    lines = cmd_result["stdout"].split("\n")[2:]
    for line in lines:
        line = line.strip()
        if not line or line.startswith("---"):
            continue
        parts = re.split(r"\s+", line)
        if len(parts) >= 4:
            disks.append({
                "type": parts[0],
                "device": parts[1],
                "target": parts[2],
                "source": parts[3] if len(parts) > 3 else ""
            })
    return disks

def get_vm_disk_actual_size(vm_name: str) -> Dict[str, Any]:
    result = {
        "vm_name": vm_name,
        "disks": [],
        "success": False,
        "error": ""
    }

    # 1. 获取disk列表
    disks = get_vm_disk_list(vm_name)
    if not disks:
        result["error"] = "未获取到虚机disk列表"
        return json.dumps(result, ensure_ascii=False, indent=2)

    # 2. 遍历disk获取大小
    for disk in disks:
        disk_info = {
            "dev": disk["target"],
            "path": disk["source"],
            "actual_size": 0,
            "virtual_size": 0,
            "usage_rate": 0.0
        }

        # qemu-img info获取大小
        if disk["source"] and os.path.exists(disk["source"]):
            img_cmd = ["qemu-img", "info", "--output", "json", disk["source"]]
            img_result = execute_cmd(img_cmd)
            if img_result["code"] != 0:
                disk_info["error"] = f"qemu-img执行失败: {img_result['stderr']}"
            else:
                try:
                    img_json = json.loads(img_result["stdout"])
                    disk_info["actual_size"] = img_json.get("actual-size", 0)
                    disk_info["virtual_size"] = img_json.get("virtual-size", 0)
                    # 计算使用率
                    if disk_info["virtual_size"] > 0:
                        disk_info["usage_rate"] = round(disk_info["actual_size"] / disk_info["virtual_size"], 4)
                except json.JSONDecodeError as e:
                    disk_info["error"] = f"JSONParse失败: {str(e)}"
        else:
            disk_info["error"] = "disksource路径为空"

        result["disks"].append(disk_info)

    result["success"] = True
    return json.dumps(result, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    import sys
    vms = get_vm_list()
    if not vms:
        print(json.dumps({"error": "No virtual machines found or virsh command failed"}, ensure_ascii=False, indent=2))
        sys.exit(1)

    results = []
    for vm in vms:
        vm_result = get_vm_disk_actual_size(vm)
        results.append(vm_result)

    # 输出所有虚机的结果（JSON数组）
    print(json.dumps(results, ensure_ascii=False, indent=2))
