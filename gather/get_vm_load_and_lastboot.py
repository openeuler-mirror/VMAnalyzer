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

if __name__ == "__main__":
    main()

