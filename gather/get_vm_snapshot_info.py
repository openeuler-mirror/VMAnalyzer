#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import json
import sys
from typing import Optional, Dict, Any
import os
import re

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

def get_vm_list() -> list:
    """获取宿主机所有虚机名称列表"""
    cmd_result = execute_cmd(["virsh", "list", "--all", "--name"])
    if cmd_result["code"] != 0:
        return []
    return [vm for vm in cmd_result["stdout"].split("\n") if vm.strip()]

"""采集虚机快照列表及详细信息"""
def get_vm_snapshot_info(vm_name: str) -> str:
    """
    获取快照名称、创建时间、状态、磁盘大小
    输出标准化快照信息列表
    """
    result = {
        "vm_name": vm_name,
        "snapshots": [],
        "success": False,
        "error": ""
    }

    # 1. 获取快照列表
    snap_list_cmd = ["virsh", "snapshot-list", vm_name]
    snap_list_result = execute_cmd(snap_list_cmd)
    if snap_list_result["code"] != 0:
        result["error"] = snap_list_result["stderr"]
        return json.dumps(result, ensure_ascii=False, indent=2)

    # 解析快照列表（跳过表头）
    lines = snap_list_result["stdout"].split("\n")[2:]
    snap_names = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("---"):
            continue
        parts = re.split(r"\s+", line)
        if len(parts) >= 1:
            snap_names.append(parts[0])

    if not snap_names:
        result["error"] = "该虚机无快照"

    # 2. 遍历快照获取详细信息
    for snap_name in snap_names:
        snap_info_cmd = ["virsh", "snapshot-info", vm_name, snap_name]
        snap_info_result = execute_cmd(snap_info_cmd)
        if snap_info_result["code"] != 0:
            continue

        snap_info = {
            "name": snap_name,
            "state": "",
            "disk_size_mb": 0,
            "is_current": False,
            "disk_size_error": ""
        }

        # 解析快照信息
        for line in snap_info_result["stdout"].split("\n"):
            line = line.strip()
            if not line or ":" not in line:
                continue
            key, value = line.split(":", 1)
            key = key.strip().lower()
            value = value.strip()

            if key == "state":
                snap_info["state"] = value
            elif key == "current":
                snap_info["is_current"] = (value.lower() == "yes")

        # 3. 获取快照磁盘大小（qemu-img）
        snap_disk_cmd = ["virsh", "snapshot-dumpxml", vm_name, snap_name]
        snap_disk_result = execute_cmd(snap_disk_cmd)
        if snap_disk_result["code"] == 0:
            disk_pattern = re.compile(r"<source file='([^']+)'")
            disk_match = disk_pattern.search(snap_disk_result["stdout"])
            if disk_match:
                disk_path = disk_match.group(1)
                img_cmd = ["qemu-img", "info", "--output", "json", disk_path]
                img_result = execute_cmd(img_cmd)
                if img_result["code"] == 0:
                    try:
                        img_json = json.loads(img_result["stdout"])
                        size = img_json.get("virtual-size", 0)
                        snap_info["disk_size_mb"] = round(size / (1024 * 1024), 2)
                    except json.JSONDecodeError as e:
                        snap_info["disk_size_error"] = f"解析qemu-img输出失败: {str(e)}"
                else:
                    # 记录qemu-img执行失败的原因
                    snap_info["disk_size_error"] = f"qemu-img执行失败: {img_result['stderr']}"

            else:
                snap_info["disk_size_error"] = "未在快照XML中找到磁盘路径"
        else:
            snap_info["disk_size_error"] = f"获取快照XML失败: {snap_disk_result['stderr']}"

        result["snapshots"].append(snap_info)

    result["success"] = True
    return json.dumps(result, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    vms = get_vm_list()
    if not vms:
        print(json.dumps({"error": "没有找到任何虚机或执行virsh命令失败"}, ensure_ascii=False, indent=2))
        sys.exit(1)

    results = []
    for vm in vms:
        try:
            vm_result_json = get_vm_snapshot_info(vm)
            vm_result = json.loads(vm_result_json)
            results.append(vm_result)
        except Exception as e:
            # 记录单个虚机处理失败的异常
            error_result = {
                "vm_name": vm,
                "snapshots": [],
                "success": False,
                "error": f"处理该虚机时发生未捕获异常: {str(e)}"
            }
            results.append(error_result)

    # 输出所有虚机的结果（JSON数组）
    print(json.dumps(results, ensure_ascii=False, indent=2))
