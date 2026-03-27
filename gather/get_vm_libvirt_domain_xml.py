#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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


def parse_xml(xml_str: str) -> Optional[etree._Element]:
    """
    解析XML字符串，返回根节点
    :param xml_str: XML内容
    :return: etree根节点 / None
    """
    try:
        return etree.fromstring(xml_str.encode("utf-8"))
    except Exception as e:
        print(f"XML解析失败: {e}")
        return None


def get_vm_list() -> list:
    """获取宿主机所有虚机名称列表"""
    cmd_result = execute_cmd(["virsh", "list", "--all", "--name"])
    if cmd_result["code"] != 0:
        return []
    return [vm for vm in cmd_result["stdout"].split("\n") if vm.strip()]

def get_vm_libvirt_domain_xml(vm_name: str, full: bool = True) -> str:
    """
    获取虚机XML配置
    :param vm_name: 虚机名称
    :param full: 是否返回完整XML（False则只返回核心节点）
    :return: JSON格式结果
    """
    result = {
        "vm_name": vm_name,
        "success": False,
        "xml": "",
        "error": ""
    }

    # 执行virsh dumpxml
    cmd = ["virsh", "dumpxml", vm_name]
    cmd_result = execute_cmd(cmd)
    if cmd_result["code"] != 0:
        result["error"] = cmd_result["stderr"]
        return json.dumps(result, ensure_ascii=False, indent=2)

    # 精简XML（可选）
    xml_content = cmd_result["stdout"]
    if not full:
        root = parse_xml(xml_content)
        if root is None:  # 解析失败时记录错误并返回
            result["error"] = f"VM {vm_name} 的XML解析失败"
            return json.dumps(result, ensure_ascii=False, indent=2)

        # 只保留核心节点（vcpu/memory/disk/interface）
        trt:
            core_nodes = ["vcpu", "memory", "disk", "interface", "os", "cpu"]
            core_xml = etree.Element("domain")
            for node in core_nodes:
                elements = root.xpath(f".//{node}")
                for elem in elements:
                    core_xml.append(elem)
            xml_content = etree.tostring(core_xml, encoding="utf-8").decode("utf-8")
        except Exception as e:
            result["error"] = f"精简VM {vm_name} 的XML时出错: {str(e)}"
            return json.dumps(result, ensure_ascii=False, indent=2)

    result["xml"] = xml_content
    result["success"] = True
    return json.dumps(result, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    import sys
    vms = get_vm_list()
    if not vms:
         print(json.dumps({"error": "没有找到任何虚机或执行virsh命令失败"}, ensure_ascii=False, indent=2))
         sys.exit(1)

    full = sys.argv[1].lower() == "true" if len(sys.argv) >= 2 else True
    results = []
    for vm in vms:
        vm_result_json = get_vm_libvirt_domain_xml(vm, full)
        vm_result = json.loads(vm_result_json)
        results.append(vm_result)

    # 输出所有虚机的结果（JSON数组）
    print(json.dumps(results, ensure_ascii=False, indent=2))
