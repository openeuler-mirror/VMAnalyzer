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
from unittest.mock import patch
import json

from gather import get_vm_qemu_agent_status

class TestVMQemuAgentStatus(unittest.TestCase):

    # =========================
    # execute_cmd
    # =========================
    @patch("gather.get_vm_qemu_agent_status.subprocess.run")
    def test_execute_cmd_success(self, mock_run):
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "ok\n"
        mock_run.return_value.stderr = ""
        result = get_vm_qemu_agent_status.execute_cmd(["ls"])
        self.assertEqual(result["code"], 0)
        self.assertEqual(result["stdout"], "ok")

    @patch("gather.get_vm_qemu_agent_status.subprocess.run")
    def test_execute_cmd_timeout(self, mock_run):
        from subprocess import TimeoutExpired
        mock_run.side_effect = TimeoutExpired(
            cmd="cmd",
            timeout=30
        )
        result = get_vm_qemu_agent_status.execute_cmd(["cmd"])
        self.assertIn("超时", result["stderr"])

    # =========================
    # get_vm_list
    # =========================
    @patch("gather.get_vm_qemu_agent_status.execute_cmd")
    def test_get_vm_list_success(self, mock_cmd):
        mock_cmd.return_value = {
            "code": 0,
            "stdout": "vm1\nvm2\n"
        }
        result = get_vm_qemu_agent_status.get_vm_list()
        self.assertEqual(result, ["vm1", "vm2"])

    @patch("gather.get_vm_qemu_agent_status.execute_cmd")
    def test_get_vm_list_fail(self, mock_cmd):
        mock_cmd.return_value = {
            "code": 1,
            "stdout": "",
            "stderr": "error"
        }
        result = get_vm_qemu_agent_status.get_vm_list()
        self.assertEqual(result, [])

    # =========================
    # get_vm_qemu_agent_status
    # =========================
    @patch("gather.get_vm_qemu_agent_status.execute_cmd")
    def test_qemu_agent_online(self, mock_cmd):
        """QGA 正常在线"""
        mock_cmd.return_value = {
            "code": 0,
            "stdout": json.dumps({
                "return": {}
            })
        }
        result_json = get_vm_qemu_agent_status.get_vm_qemu_agent_status("vm1")
        result = json.loads(result_json)
        self.assertTrue(result["success"])
        self.assertTrue(result["agent_online"])
        self.assertEqual(result["vm_name"], "vm1")

    @patch("gather.get_vm_qemu_agent_status.execute_cmd")
    def test_qemu_agent_offline(self, mock_cmd):
        """命令执行失败"""
        mock_cmd.return_value = {
            "code": 1,
            "stderr": "guest agent not running",
            "stdout": ""
        }

if __name__ == "__main__":
    unittest.main()
