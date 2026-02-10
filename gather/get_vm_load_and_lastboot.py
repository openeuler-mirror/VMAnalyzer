#!/usr/bin/env python3
import subprocess
import json
import logging
import time
import argparse
import os
from datetime import datetime
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class VMSysMonitor:
    def __init__(self, poll: int = 60, out_dir: str = "./vm_sys_data"):
        self.poll = poll
        self.out_dir = out_dir
        os.makedirs(out_dir, exist_ok=True)
        self.data = {"collect_time": "", "vm_count": 0, "vms": {}}

    def _run_cmd(self, cmd: str) -> Optional[str]:
        try:
            # 核心修复：用universal_newlines替代text，兼容Python3.6及以下
            res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                universal_newlines=True, check=True, timeout=30)
            return res.stdout.strip() or None
        except subprocess.CalledProcessError as e:
            err = e.stderr.strip()
            if "not supported" not in err.lower() and "unknown command" not in err.lower():
                logger.error(f"Cmd fail: {cmd} | Err: {err}")
            return None
        except Exception as e:
            logger.error(f"Cmd err: {cmd} | Err: {str(e)}")
            return None

    def get_running_vms(self) -> List[str]:
        cmd = "virsh list --name | grep -v '^$'"
        output = self._run_cmd(cmd)
        return output.split() if output else []

    def get_boot_time(self, vm: str) -> str:
        cmd = f"virsh qemu-agent-command {vm} '{{\"execute\":\"guest-get-lastboot-time\"}}'"
        res = self._run_cmd(cmd)
        if not res:
            return "采集失败"
        try:
            return json.loads(res)["return"]["lastboot"].strip()
        except:
            return "解析失败"

    def get_load_avg(self, vm: str) -> Dict:
        cmd = f"virsh qemu-agent-command {vm} '{{\"execute\":\"guest-get-load-average\"}}'"
        res = self._run_cmd(cmd)
        load = {"1min": "N/A", "5min": "N/A", "15min": "N/A", "note": "不支持/采集失败"}
        if res:
            try:
                d = json.loads(res)["return"]
                load = {
                    "1min": d.get("load1-average", "N/A").strip(),
                    "5min": d.get("load5-average", "N/A").strip(),
                    "15min": d.get("load15-average", "N/A").strip(),
                    "note": "采集成功"
                }
            except:
                load["note"] = "解析失败"
        return load

    def collect(self) -> None:
        self.data["collect_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        vms = self.get_running_vms()
        self.data["vm_count"] = len(vms)
        for vm in vms:
            logger.info(f"Collecting {vm}...")
            self.data["vms"][vm] = {
                "boot_time": self.get_boot_time(vm),
                "load_avg": self.get_load_avg(vm),
                "status": "success" if self.get_boot_time(vm) != "采集失败" else "fail"
            }


if __name__ == "__main__":
    main()

