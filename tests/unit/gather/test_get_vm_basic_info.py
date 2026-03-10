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
        self.mock_domstate_running = "running"
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
        with patch("subprocess.run") as mock_subprocess:
            mock_subprocess.side_effect = subprocess.CalledProcessError(
                returncode=1,
                cmd=test_cmd.split(),
                stderr="Domain not found"
            )
            result = self.monitor.run_virsh_cmd(test_cmd)
            self.assertIsNone(result)

    def test_get_all_vm_names(self):
        mock_output = "\n".join(self.test_vm_names)
        with patch.object(self.monitor, "run_virsh_cmd", return_value=mock_output) as mock_run_cmd:
            vm_names = self.monitor.get_all_vm_names()
            self.assertEqual(vm_names, self.test_vm_names)
            mock_run_cmd.assert_called_once_with("virsh list --all --name")

    def test_parse_domstate(self):
        with patch.object(self.monitor, "run_virsh_cmd", return_value=self.mock_domstate_running) as mock_run_cmd:
            state = self.monitor.parse_domstate(self.test_vm_name)
            self.assertEqual(state, self.mock_domstate_running)
            mock_run_cmd.assert_called_once_with(f"virsh domstate {self.test_vm_name}")
        with patch.object(self.monitor, "run_virsh_cmd", return_value=None) as mock_run_cmd:
            state = self.monitor.parse_domstate(self.test_vm_name)
            self.assertEqual(state, "unknown")

    def test_parse_domtime(self):
        with patch.object(self.monitor, "run_virsh_cmd", return_value=self.mock_domtime_output) as mock_run_cmd:
            domtime = self.monitor.parse_domtime(self.test_vm_name)
            self.assertEqual(domtime["utc_time"], "2026-02-05 10:00:00")
            self.assertEqual(domtime["local_time"], "2026-02-05 18:00:00")
            self.assertEqual(domtime["time_offset"], "28800 seconds")
            mock_run_cmd.assert_called_once_with(f"virsh domtime {self.test_vm_name}")
        with patch.object(self.monitor, "run_virsh_cmd", return_value=None):
            domtime = self.monitor.parse_domtime(self.test_vm_name)
            self.assertEqual(domtime, {})

if __name__ == "__main__":
    unittest.main(verbosity=2)
