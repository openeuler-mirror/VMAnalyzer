#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""判断虚机是否崩溃"""
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

"""采集虚机Libvirt UUID（无XML依赖）"""
def get_vm_basic_info(vm_name: str) -> Dict[str, Any]:
    result = {
        "vm_name": vm_name,
        "uuid": "",
        "state": "",
        "error": ""
    }
    cmd = ["virsh", "dominfo", vm_name]
    cmd_result = execute_cmd(cmd)
    if cmd_result["code"] != 0:
        result["error"] = cmd_result["stderr"]
        return result

    # 解析dominfo输出
    for line in cmd_result["stdout"].split("\n"):
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip().lower()
        value = value.strip()
        if key == "uuid":
            result["uuid"] = value
        elif key == "state":
            result["state"] = value
    return result

def get_vm_libvirt_uuid(vm_name: str) -> str:
    """获取并校验虚机UUID"""
    result = {
        "vm_name": vm_name,
        "uuid": "",
        "uuid_valid": False,
        "success": False,
        "error": ""
    }

    basic_info = get_vm_basic_info(vm_name)
    if basic_info["error"]:
        result["error"] = basic_info["error"]
        return json.dumps(result, ensure_ascii=False, indent=2)

    # 提取并校验UUID
    uuid = basic_info["uuid"]
    uuid_pattern = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)
    result["uuid"] = uuid
    result["uuid_valid"] = bool(uuid_pattern.match(uuid))
    result["success"] = True
    return json.dumps(result, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python get_vm_libvirt_uuid.py <vm-name>")
        sys.exit(1)
    print(get_vm_libvirt_uuid(sys.argv[1]))
