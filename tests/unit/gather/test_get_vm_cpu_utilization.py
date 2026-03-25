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
        result = self.collector.call_qga_interface(
            "vm1",
            "guest-get-cpu-utilization"
        )
        self.assertEqual(result["status"], "failed")

    @patch.object(get_vm_cpu_utilization.VMCollector, "run_virsh_cmd")
    def test_qga_parse_error(self, mock_cmd):
        mock_cmd.return_value = "invalid json"
        result = self.collector.call_qga_interface(
            "vm1",
            "guest-get-cpu-utilization"
        )
        self.assertEqual(result["status"], "parse_error")

class TestCollectVM(unittest.TestCase):
    def setUp(self):
        self.collector = get_vm_cpu_utilization.VMCollector()

    @patch.object(get_vm_cpu_utilization.VMCollector, "call_qga_interface")
    @patch.object(get_vm_cpu_utilization.VMCollector, "get_vm_state")
    def test_collect_running_vm(self, mock_state, mock_qga):
        mock_state.return_value = "running"
        mock_qga.return_value = {
            "status": "success",
            "data": {"cpu": 20},
            "error": ""
        }
        result = self.collector.collect_single_vm_data("vm1")
        self.assertEqual(result["state"], "running")
        self.assertEqual(
            result["get_cpu_utilization"]["data"],
            {"cpu": 20}
        )

    @patch.object(get_vm_cpu_utilization.VMCollector, "get_vm_state")
    def test_collect_shutdown_vm(self, mock_state):
        mock_state.return_value = "shut off"
        result = self.collector.collect_single_vm_data("vm1")
        self.assertEqual(
            result["get_cpu_utilization"]["interface"],
            "guest-get-cpu-utilization"
        )

class TestCollectAll(unittest.TestCase):
    @patch.object(get_vm_cpu_utilization.VMCollector, "collect_single_vm_data")
    @patch.object(get_vm_cpu_utilization.VMCollector, "get_all_vm_names")
    def test_collect_all_vms(self, mock_names, mock_collect):
        mock_names.return_value = ["vm1", "vm2"]
        mock_collect.side_effect = [
            {"name": "vm1"},
            {"name": "vm2"}
        ]
        collector = get_vm_cpu_utilization.VMCollector()
        collector.collect_all_vms()
        self.assertEqual(
            len(collector.all_vms_data["vms"]),
            2
        )

class TestSaveData(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open)
    @patch("gather.get_vm_cpu_utilization.datetime")
    def test_save_data(self, mock_datetime, mock_file):
        mock_datetime.now.return_value.strftime.return_value = "20240101_120000"
