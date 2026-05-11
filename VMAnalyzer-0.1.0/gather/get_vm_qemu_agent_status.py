#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""采集QEMU Guest Agent状态"""
import json
import subprocess
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

def get_vm_list() -> list:
    """获取宿主机所有虚机名称列表"""
    cmd_result = execute_cmd(["virsh", "list", "--all", "--name"])
    if cmd_result["code"] != 0:
        return []
    return [vm for vm in cmd_result["stdout"].split("\n") if vm.strip()]

def get_vm_qemu_agent_status(vm_name: str) -> str:
    """
    检查QGA连通性
    :param vm_name: 虚机名称
    :return: JSON格式结果
    """
    result = {
        "vm_name": vm_name,
        "agent_online": False,
        "success": False,
        "error": ""
    }

    ping_cmd = ["virsh", "qemu-agent-command", vm_name, '{"execute":"guest-ping"}']
    ping_result = execute_cmd(ping_cmd)
    if ping_result["code"] != 0:
        result["error"] = f"QGA连通性检测失败: {ping_result['stderr']}"
        return json.dumps(result, ensure_ascii=False, indent=2)

    try:
        ping_json = json.loads(ping_result["stdout"])
        if "return" in ping_json:
            result["agent_online"] = True

    except json.JSONDecodeError:
        result["error"] = "QGA返回结果解析失败"

    result["success"] = True
    return json.dumps(result, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    import sys
    vms = get_vm_list()
    if not vms:
         print(json.dumps({"error": "没有找到任何虚机或执行virsh命令失败"}, ensure_ascii=False, indent=2))
         sys.exit(1)

    results = []
    for vm in vms:
        # 调用已有的获取XML函数，它返回JSON字符串，我们需要解析为字典
        vm_result_json = get_vm_qemu_agent_status(vm)
        vm_result = json.loads(vm_result_json)
        results.append(vm_result)

    # 输出所有虚机的结果（JSON数组）
    print(json.dumps(results, ensure_ascii=False, indent=2))
