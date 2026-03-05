#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
import time
import subprocess
from unittest.mock import patch, MagicMock, mock_open
from gather import get_vm_basic_info as vm_monitor

class TestVMDomainMonitor(unittest.TestCase):
    """
    虚拟机基础信息采集类的单元测试
    """

    def setUp(self):
        self.monitor = vm_monitor.VMDomainMonitor()
        self.test_vm_name = "vm-test-01"
        self.test_vm_names = ["vm-test-01", "vm-test-02"]
    def tearDown(self):
        self.monitor = None

    def test_run_virsh_cmd_success(self):
        test_cmd = "virsh list --all --name"
        mock_output = "\n".join(self.test_vm_names)
        with patch("subprocess.run") as mock_subprocess:
            mock_result = MagicMock()
            mock_result.stdout.strip.return_value = mock_output
            mock_result.returncode = 0
            mock_subprocess.return_value = mock_result
            result = self.monitor.run_virsh_cmd(test_cmd)
            result = self.monitor.run_virsh_cmd(test_cmd)
            self.assertEqual(result, mock_output)
            mock_subprocess.assert_called_once_with(
                test_cmd.split(),
                capture_output=True,
                text=True,
                check=True
            )

    def test_run_virsh_cmd_fail(self):
        test_cmd = "virsh domstate non-exist-vm"

if __name__ == "__main__":
    unittest.main(verbosity=2)
