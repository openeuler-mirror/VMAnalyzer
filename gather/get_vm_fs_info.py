#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import libvirt
import json
import logging
import sys
import time
from typing import List, Dict

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
LOG_INFO = logging.info
LOG_ERROR = logging.error

class VMAnalyzer:
    def parse_fsinfo(self, raw_fsinfo: List[tuple]) -> List[Dict]:
        parsed_fs_list = []
        for fs in raw_fsinfo:
            volume_name = fs[0] if len(fs) > 0 else "Unknown"
            volume_uuid_path = fs[1] if len(fs) > 1 else ""
            fs_type = fs[2] if len(fs) > 2 else "Unknown"
            device = fs[3][0] if len(fs) > 3 and fs[3] else "Unknown"
            parsed_fs = {
                "volume_name": volume_name,
                "volume_path": volume_uuid_path,
                "fs_type": fs_type,
                "device": device,
                "mount_point": volume_name,
                "is_system_volume": volume_name in ["System Reserved", "C:\\"]
            }
            parsed_fs_list.append(parsed_fs)
        print(parsed_fs_list)
        return parsed_fs_list

if __name__ == "__main__":
    main()

