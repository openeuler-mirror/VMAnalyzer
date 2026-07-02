#!/usr/bin/env python3
# _*_coding: utf-8 _*_
"""采集虚机网络接口包丢弃统计"""
import subprocess
import json
import re
from typing import Dict, Any

def execute_cmd(cmd: list, timeout: int = 30) -> Dict[str, Any]:
    """执行系统命令，返回标准化结果"""
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

def get_vm_network_drops(vm_name: str) -> Dict[str, Any]:
    """
    获取虚机网络接口包丢弃统计
    :param vm_name: 虚机名称
    :return: 网络丢弃统计信息
    """
    result = {
        "vm_name": vm_name,
        "interfaces": [],
        "timestamp": None
    }
    
    try:
        # 获取接口统计信息
        cmd_result = execute_cmd(["virsh", "domifstat", vm_name])
        if cmd_result["code"] != 0:
            result["error"] = cmd_result["stderr"]
            return result
        
        iface_stats = {}
        for line in cmd_result["stdout"].split("\n"):
            parts = line.split()
            if len(parts) >= 3:
                iface_name = parts[0]
                metric = parts[1]
                value = parts[2]
                
                if iface_name not in iface_stats:
                    iface_stats[iface_name] = {}
                
                # 关注丢弃和错误相关的指标
                if "drop" in metric.lower() or "err" in metric.lower():
                    iface_stats[iface_name][metric] = value
        
        for iface, stats in iface_stats.items():
            result["interfaces"].append({
                "interface": iface,
                "stats": stats
            })
        
        from datetime import datetime
        result["timestamp"] = datetime.now().isoformat()
        
    except Exception as e:
        result["error"] = str(e)
    
    return result

def main():
    """主函数"""
    vm_list = get_vm_list()
    results = []
    
    for vm_name in vm_list:
        vm_stats = get_vm_network_drops(vm_name)
        results.append(vm_stats)
    
    print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
