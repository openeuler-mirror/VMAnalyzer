#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import subprocess
import json
from lxml import etree
from typing import Optional, Dict, Any

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

def get_vm_qemu_agent_version(vm_name: str) -> str:
    """
    检查QGA连通性+获取版本
    :param vm_name: 虚机名称
    :return: JSON格式结果
    """
    result = {
        "vm_name": vm_name,
        "agent_version": "",
        "success": False,
        "error": ""
    }

    version_cmd = ["virsh", "qemu-agent-command", vm_name, '{"execute":"guest-info"}']
    version_result = execute_cmd(version_cmd)
    if version_result["code"] == 0:
        version_json = json.loads(version_result["stdout"])
        result["agent_version"] = version_json.get("return", {}).get("version", "")

    result["success"] = True
    return json.dumps(result, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python get_vm_qemu_agent_status.py <vm-name>")
        sys.exit(1)
    print(get_vm_qemu_agent_version(sys.argv[1]))
