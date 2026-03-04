#!/usr/bin/env python3
# _*_coding: utf-8 _*_

# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of
# the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#          http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.
import unittest
import os
import json
import shutil
import subprocess
from datetime import datetime
from unittest.mock import patch, MagicMock

from gather.get_vm_load_and_lastboot import VMSysMonitor, logger

class TestGetVMLoadAndLastboot(unittest.TestCase):
    """VM负载和最后启动时间采集模块单测"""
    def setUp(self):
        self.poll_interval = 1
        test_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.test_out_dir = os.path.join(test_root, "temp", "test_vm_load_lastboot")

        class TestableVMSysMonitor(VMSysMonitor):
            def call_run_cmd(self, cmd):
                return super()._run_cmd(cmd)

        self.monitor = TestableVMSysMonitor(poll=self.poll_interval, out_dir=self.test_out_dir)

if __name__ == "__main__":
    unittest.main(verbosity=2)
