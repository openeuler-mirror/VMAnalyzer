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
from unittest.mock import patch, MagicMock, mock_open
import subprocess
import json

from gather import get_vm_cpu_utilization

class TestRunVirshCmd(unittest.TestCase):
    @patch("gather.get_vm_cpu_utilization.subprocess.run")
    def test_run_cmd_success(self, mock_run):
        mock_result = MagicMock()
        mock_result.stdout = "test output\n"
        mock_run.return_value = mock_result
        collector = get_vm_cpu_utilization.VMCollector()
        result = collector.run_virsh_cmd("virsh list")
        self.assertEqual(result, "test output")

    @patch("gather.get_vm_cpu_utilization.subprocess.run")
    def test_run_cmd_error(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(
            1, "virsh", stderr="error"
        )
        collector = get_vm_cpu_utilization.VMCollector()
        result = collector.run_virsh_cmd("virsh list")
        self.assertIsNone(result)

    @patch("gather.get_vm_cpu_utilization.subprocess.run")
    def test_run_cmd_timeout(self, mock_run):
        mock_run.side_effect = subprocess.TimeoutExpired("virsh", 30)
        collector = get_vm_cpu_utilization.VMCollector()
        result = collector.run_virsh_cmd("virsh list")
        self.assertIsNone(result)

class TestVMInfo(unittest.TestCase):
    def setUp(self):
        self.collector = get_vm_cpu_utilization.VMCollector()

    @patch.object(get_vm_cpu_utilization.VMCollector, "run_virsh_cmd")
    def test_get_all_vm_names(self, mock_cmd):
        mock_cmd.return_value = "vm1\nvm2\n"
        result = self.collector.get_all_vm_names()
        self.assertEqual(result, ["vm1", "vm2"])

    @patch.object(get_vm_cpu_utilization.VMCollector, "run_virsh_cmd")
    def test_get_vm_state(self, mock_cmd):
        mock_cmd.return_value = "running"
        result = self.collector.get_vm_state("vm1")
        self.assertEqual(result, "running")

class TestQGA(unittest.TestCase):
    def setUp(self):
        self.collector = get_vm_cpu_utilization.VMCollector()

    @patch.object(get_vm_cpu_utilization.VMCollector, "run_virsh_cmd")
    def test_qga_success(self, mock_cmd):
        mock_cmd.return_value = json.dumps({
            "return": {"cpu": 10}
        })
        result = self.collector.call_qga_interface(
            "vm1",
            "guest-get-cpu-utilization"
        )
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"], {"cpu": 10})

    @patch.object(get_vm_cpu_utilization.VMCollector, "run_virsh_cmd")
    def test_qga_error(self, mock_cmd):
        mock_cmd.return_value = json.dumps({
            "error": {"message": "failed"}
        })
