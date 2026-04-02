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
from unittest.mock import patch, MagicMock, mock_open
import json

from gather import get_vm_oom_status

class TestVMOOMCollector(unittest.TestCase):

    def setUp(self):
        self.collector = get_vm_oom_status.VMCollector(
            output_dir="./test_output"
        )

    # =========================
    # run_virsh_cmd
    # =========================
    @patch("gather.get_vm_oom_status.subprocess.run")
    def test_run_virsh_cmd_success(self, mock_run):
        mock_run.return_value = MagicMock(
            stdout="ok\n",
            stderr="",
            returncode=0
        )
        result = self.collector.run_virsh_cmd("virsh list")
        self.assertEqual(result, "ok")

    @patch("gather.get_vm_oom_status.subprocess.run")
    def test_run_virsh_cmd_called_process_error(self, mock_run):
        from subprocess import CalledProcessError
        mock_run.side_effect = CalledProcessError(
            returncode=1,
            cmd="virsh fail",
            stderr="some error"
        )
        result = self.collector.run_virsh_cmd("virsh fail")
        self.assertIsNone(result)

    @patch("gather.get_vm_oom_status.subprocess.run")
    def test_run_virsh_cmd_timeout(self, mock_run):
        from subprocess import TimeoutExpired
        mock_run.side_effect = TimeoutExpired(
            cmd="virsh list",
            timeout=30
        )
        result = self.collector.run_virsh_cmd("virsh list")
        self.assertIsNone(result)

    # =========================
    # get_all_vm_names
    # =========================
    @patch.object(get_vm_oom_status.VMCollector, "run_virsh_cmd")
    def test_get_all_vm_names_success(self, mock_run):
        mock_run.return_value = "vm1 vm2 vm3"
        result = self.collector.get_all_vm_names()
        self.assertEqual(result, ["vm1", "vm2", "vm3"])

    @patch.object(get_vm_oom_status.VMCollector, "run_virsh_cmd")
    def test_get_all_vm_names_empty(self, mock_run):
        mock_run.return_value = None
        result = self.collector.get_all_vm_names()
        self.assertEqual(result, [])

    # =========================
    # call_qga_interface
    # =========================
    @patch.object(get_vm_oom_status.VMCollector, "run_virsh_cmd")
    def test_call_qga_interface_success(self, mock_run):
        mock_run.return_value = json.dumps({
            "return": {
                "oom-kill": False
            }
        })
        result = self.collector.call_qga_interface(
            "vm1",
            "guest-get-oom-status"
        )
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"]["oom-kill"], False)

    @patch.object(get_vm_oom_status.VMCollector, "run_virsh_cmd")
    def test_call_qga_interface_failed(self, mock_run):
        mock_run.return_value = json.dumps({
            "error": {
                "message": "not supported"
            }
        })
        result = self.collector.call_qga_interface(
            "vm1",
            "guest-get-oom-status"
        )
        self.assertEqual(result["status"], "failed")

    @patch.object(get_vm_oom_status.VMCollector, "run_virsh_cmd")
    def test_call_qga_interface_parse_error(self, mock_run):
        mock_run.return_value = "invalid json"
        result = self.collector.call_qga_interface(
            "vm1",
            "guest-get-oom-status"
        )
        self.assertEqual(result["status"], "parse_error")

    @patch.object(get_vm_oom_status.VMCollector, "run_virsh_cmd")
    def test_call_qga_interface_no_output(self, mock_run):
        mock_run.return_value = None
        result = self.collector.call_qga_interface(
            "vm1",
            "guest-get-oom-status"
        )
        self.assertEqual(result["status"], "failed")

    # =========================
    # collect_single_vm_data
    # =========================

    @patch.object(get_vm_oom_status.VMCollector, "call_qga_interface")
    def test_collect_single_vm_data(self, mock_call):
        mock_call.return_value = {
            "status": "success",
            "data": {"oom-kill": False},
            "error": ""
        }
        result = self.collector.collect_single_vm_data("vm1")
        self.assertEqual(result["name"], "vm1")
        self.assertIn("get_oom_status", result)

if __name__ == "__main__":
    unittest.main()
