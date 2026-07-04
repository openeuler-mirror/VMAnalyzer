#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取VM CPU 缓存拓扑信息
输出 L1/L2/L3 大小、NUMA 节点亲和性
"""

import subprocess
import json
import logging
import argparse
import time
from typing import Dict, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
LOG_INFO = logging.info
LOG_ERROR = logging.error


def run_virsh_cmd(cmd: str) -> Optional[str]:
    """执行 virsh 命令并返回标准输出"""
    try:
        LOG_INFO(f"Executing command：{cmd}")
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            universal_newlines=True,
            timeout=30
        )
        if result.returncode != 0:
            LOG_ERROR(f"命令失败：{result.stderr.strip()}")
            return None
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        LOG_ERROR("Command timed out")
        return None
    except Exception as e:
        LOG_ERROR(f"Executing command异常：{e}")
        return None


def get_domain_xml(vm_name: str) -> Optional[str]:
    """获取VM XML 配置"""
    cmd = f"virsh dumpxml {vm_name}"
    return run_virsh_cmd(cmd)


def parse_cpu_cache_from_xml(xml: str) -> Dict:
    """
    从 XML 中提取 CPU 模型、拓扑、NUMA、缓存信息
    返回结构化字典
    """
    import xml.etree.ElementTree as ET
    data = {
        "cpu_model": "",
        "topology": {},
        "cache": {},
        "numa": {}
    }
    try:
        root = ET.fromstring(xml)
        # Implementation note.
        cpu_elem = root.find("cpu")
        if cpu_elem is not None:
            model_elem = cpu_elem.find("model")
            if model_elem is not None:
                data["cpu_model"] = model_elem.text or ""
            # Implementation note.
            topo = cpu_elem.find("topology")
            if topo is not None:
                data["topology"] = {
                    "sockets": int(topo.get("sockets", 0)),
                    "cores": int(topo.get("cores", 0)),
                    "threads": int(topo.get("threads", 0))
                }
            # Implementation note.
            for cache in cpu_elem.findall("cache"):
                level = cache.get("level")
                if level:
                    data["cache"][f"L{level}"] = {
                        "size": cache.get("size", "unknown"),
                        "unit": cache.get("unit", "KiB"),
                        "type": cache.get("type", "unknown"),
                        "associativity": cache.get("associativity", "unknown")
                    }
            # NUMA
            numa = cpu_elem.find("numa")
            if numa is not None:
                for cell in numa.findall("cell"):
                    cid = cell.get("id")
                    if cid:
                        data["numa"][cid] = {
                            "cpus": cell.get("cpus", ""),
                            "memory": cell.get("memory", "0"),
                            "unit": cell.get("unit", "KiB")
                        }
    except ET.ParseError as e:
        LOG_ERROR(f"XML Parse失败：{e}")
    return data


def get_vm_cpu_cache_topology(vm_name: str) -> Dict:
    """主入口：返回单台 VM 的 CPU 缓存拓扑信息"""
    xml = get_domain_xml(vm_name)
    if not xml:
        return {}
    data = parse_cpu_cache_from_xml(xml)
    data["vm_name"] = vm_name
    data["timestamp"] = int(time.time())
    return data


def main():
    parser = argparse.ArgumentParser(description="获取VM CPU 缓存拓扑信息")
    parser.add_argument("vm_name", help="VM名称")
    parser.add_argument("-o", "--output", help="可选：输出 JSON 文件路径")
    args = parser.parse_args()

    info = get_vm_cpu_cache_topology(args.vm_name)
    if not info:
        LOG_ERROR("无法获取信息，请确认VM存在且 virsh 可访问")
        return

    print(json.dumps(info, indent=2, ensure_ascii=False))

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(info, f, indent=2, ensure_ascii=False)
        LOG_INFO(f"结果已写入 {args.output}")


if __name__ == "__main__":
    main()
