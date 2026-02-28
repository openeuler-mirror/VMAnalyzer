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

def get_vm_disk_list(vm_name: str) -> list:
    """获取虚机磁盘列表"""
    disks = []
    cmd = ["virsh", "domblklist", vm_name, "--details"]
    cmd_result = execute_cmd(cmd)
    if cmd_result["code"] != 0:
        return disks

    # 解析domblklist输出（跳过表头）
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

"""采集虚机磁盘IO错误次数"""
def get_vm_disk_io_error_count(vm_name: str) -> str:
    result = {
        "vm_name": vm_name,
        "disks": [],
        "success": False,
        "error": ""
    }

    # 1. 获取磁盘列表
    disks = get_vm_disk_list(vm_name)
    if not disks:
        result["error"] = "未获取到虚机磁盘列表"
        return json.dumps(result, ensure_ascii=False, indent=2)

    # 2. 遍历磁盘获取错误数
    for disk in disks:
        dev = disk["target"]
        if not dev:
            continue

        error_info = {
            "dev": dev,
            "read_errors": 0,
            "write_errors": 0,
            "flush_errors": 0
        }

        # 执行virsh domblkerror
        blk_cmd = ["virsh", "domblkerror", vm_name, dev]
        blk_result = execute_cmd(blk_cmd)
        if blk_result["code"] == 0:
            # 解析输出
            for line in blk_result["stdout"].split("\n"):
                line = line.strip()
                if "Read errors:" in line:
                    error_info["read_errors"] = int(line.split(":")[1].strip())
                elif "Write errors:" in line:
                    error_info["write_errors"] = int(line.split(":")[1].strip())
                elif "Flush errors:" in line:
                    error_info["flush_errors"] = int(line.split(":")[1].strip())

        result["disks"].append(error_info)

    result["success"] = True
    return json.dumps(result, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python get_vm_disk_io_error_count.py <vm-name>")
        sys.exit(1)
    print(get_vm_disk_io_error_count(sys.argv[1]))
