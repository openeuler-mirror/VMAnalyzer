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
from unittest.mock import patch, MagicMock
import subprocess
import json

from gather import get_vm_state

class TestGetVMState(unittest.TestCase):
    # =========================
    # execute_cmd
    # =========================
    @patch("gather.get_vm_state.subprocess.run")
    def test_execute_cmd_success(self, mock_run):
        """测试 execute_cmd 成功"""
        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.stdout = "running\n"
        mock_proc.stderr = ""
        mock_run.return_value = mock_proc
        result = get_vm_state.execute_cmd(["ls"])
        self.assertEqual(result["code"], 0)
        self.assertEqual(result["stdout"], "running")
        self.assertEqual(result["stderr"], "")

    @patch("gather.get_vm_state.subprocess.run")
    def test_execute_cmd_timeout(self, mock_run):
        """测试 execute_cmd 超时"""
        mock_run.side_effect = subprocess.TimeoutExpired(
            cmd=["ls"],
            timeout=30
        )
        result = get_vm_state.execute_cmd(["ls"])
        self.assertEqual(result["code"], -1)
        self.assertIn("命令执行超时", result["stderr"])

    @patch("gather.get_vm_state.subprocess.run")
    def test_execute_cmd_exception(self, mock_run):
        """测试 execute_cmd 异常"""
        mock_run.side_effect = Exception("run error")
            result = get_vm_state.execute_cmd(["ls"])
        self.assertEqual(result["code"], -1)
        self.assertIn("命令执行异常", result["stderr"])

    # =========================
    # get_vm_list
    # =========================
    @patch("gather.get_vm_state.execute_cmd")
    def test_get_vm_list_success(self, mock_exec):
        """测试获取虚机列表成功"""
        mock_exec.return_value = {
            "code": 0,
            "stdout": "vm1\nvm2\n",
            "stderr": ""
        }
        result = get_vm_state.get_vm_list()
        self.assertEqual(result, ["vm1", "vm2"])

    @patch("gather.get_vm_state.execute_cmd")
    def test_get_vm_list_failed(self, mock_exec):
        """测试获取虚机列表失败"""
        mock_exec.return_value = {
            "code": 1,
            "stdout": "",
            "stderr": "error"
        }

if __name__ == "__main__":
    unittest.main()
