#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import json
import logging
import time
import argparse
import os
from datetime import datetime
from typing import Dict, List, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


class VMMemTopNCollector:
    def __init__(self, top_n: int = 5, poll_interval: int = 60, output_dir: str = "./vm_mem_topn_data"):
        self.top_n = top_n
        self.poll_interval = poll_interval
        self.output_dir = output_dir
        self._init_output_dir()

        self.collect_data = {
            "collect_time": "",
            "running_vm_count": 0,
            "vm_list": {}
        }

    def _init_output_dir(self) -> None:
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)

    def _exec_virsh_cmd(self, cmd: str) -> Optional[str]:
        try:
            logger.info(f"执行命令：{cmd}")
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                universal_newlines=True,
                check=True,
                timeout=30
            )
            output = result.stdout.strip()
            return output if output else None

        except subprocess.CalledProcessError as e:
            err_msg = e.stderr.strip()
            logger.error(f"命令执行失败：{cmd}，错误：{err_msg}")
            return None

        except subprocess.TimeoutExpired:
            logger.error(f"命令执行超时：{cmd}（超过30秒）")
            return None

        except Exception as e:
            logger.error(f"命令执行异常：{cmd}，错误：{str(e)}")
            return None

    def get_running_vms(self) -> List[str]:
        cmd = "virsh list --name | grep -v '^$'"
        output = self._exec_virsh_cmd(cmd)
        return output.split() if output else []

    def get_vm_mem_topn(self, vm_name: str) -> Optional[List[Dict]]:
        qga_params = {
            "execute": "guest-get-memtopn-status",
            "arguments": {"memtopn-num": str(self.top_n)}
        }
        qga_cmd = f"virsh qemu-agent-command {vm_name} '{json.dumps(qga_params)}'"
        output = self._exec_virsh_cmd(qga_cmd)

        if not output:
            logger.error(f"VM {vm_name} 内存TopN信息采集失败：无返回数据")
            return None

        try:
            resp = json.loads(output)
            if "return" not in resp:
                logger.error(f"VM {vm_name} QGA返回格式异常：{output}")
                return None
            return resp["return"]

        except json.JSONDecodeError as e:
            logger.error(f"VM {vm_name} QGA返回解析失败：{str(e)}，原始数据：{output}")
            return None


if __name__ == "__main__":
    try:
        from typing import Dict, List, Optional
    except ImportError:
        pass

    main()

