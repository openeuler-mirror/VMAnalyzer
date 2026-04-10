#!/usr/bin/env python3
# _*_coding: utf-8 _*_
"""采集虚机Libvirt生命周期状态"""
import json
import subprocess
import sys
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

def get_vm_state(vm_name: str) -> str:
    """
    获取虚机状态（标准化编码）
    状态映射：
    running(1)-运行中, paused(2)-暂停, shut off(0)-关机,
    crashed(-1)-崩溃, migrating(3)-迁移中, unknown(-2)-未知
    :param vm_name: 虚机名称
    :return: JSON格式结果
    """
    result = {
        "vm_name": vm_name,
        "state_code": -2,
        "state_desc": "未知状态",
        "success": False,
        "error": ""
    }

    # 执行virsh domstate
    cmd = ["virsh", "domstate", vm_name]
    cmd_result = execute_cmd(cmd)
    if cmd_result["code"] != 0:
        result["error"] = cmd_result["stderr"]
        return json.dumps(result, ensure_ascii=False, indent=2)

    # 状态映射
    state_raw = cmd_result["stdout"].lower()
    state_mapping = {
        "running": (1, "运行中"),
        "paused": (2, "已暂停"),
        "shut off": (0, "已关机"),
        "crashed": (-1, "已崩溃"),
        "migrating": (3, "迁移中"),
        "suspended": (2, "已挂起"),
        "blocked": (-3, "阻塞中")
    }

    if state_raw in state_mapping:
        result["state_code"], result["state_desc"] = state_mapping[state_raw]
    result["success"] = True
    return json.dumps(result, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    vms = get_vm_list()
    if not vms:
         print(json.dumps({"error": "没有找到任何虚机或执行virsh命令失败"}, ensure_ascii=False, indent=2))
         sys.exit(1)

    results = []
    for vm in vms:
        vm_result_json = get_vm_state(vm)
        vm_result = json.loads(vm_result_json)
        results.append(vm_result)

    # 输出所有虚机的结果（JSON数组）
    print(json.dumps(results, ensure_ascii=False, indent=2))
