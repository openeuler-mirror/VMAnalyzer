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

from gather import get_vm_disk_iops

class TestGetVMDiskIOPS(unittest.TestCase):

    # =========================
    # execute_cmd
    # =========================
    @patch("gather.get_vm_disk_iops.subprocess.run")
    def test_execute_cmd_success(self, mock_run):
        """测试 execute_cmd 成功"""
        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.stdout = "ok\n"
        mock_proc.stderr = ""
        mock_run.return_value = mock_proc
        result = get_vm_disk_iops.execute_cmd(["ls"])
        self.assertEqual(result["code"], 0)
        self.assertEqual(result["stdout"], "ok")
        self.assertEqual(result["stderr"], "")

    @patch("gather.get_vm_disk_iops.subprocess.run")
    def test_execute_cmd_timeout(self, mock_run):
        """测试 execute_cmd 超时"""
        mock_run.side_effect = subprocess.TimeoutExpired(
            cmd=["ls"],
            timeout=30
        )
        result = get_vm_disk_iops.execute_cmd(["ls"])
        self.assertEqual(result["code"], -1)
        self.assertIn("命令执行超时", result["stderr"])

    @patch("gather.get_vm_disk_iops.subprocess.run")
    def test_execute_cmd_exception(self, mock_run):
        """测试 execute_cmd 异常"""
        mock_run.side_effect = Exception("run error")
        result = get_vm_disk_iops.execute_cmd(["ls"])
        self.assertEqual(result["code"], -1)
        self.assertIn("命令执行异常", result["stderr"])

    # =========================
    # get_vm_list
    # =========================
    @patch("gather.get_vm_disk_iops.execute_cmd")
    def test_get_vm_list_success(self, mock_exec):
        """测试获取虚机列表成功"""
        mock_exec.return_value = {
            "code": 0,
            "stdout": "vm1\nvm2\n",
            "stderr": ""
        }
        result = get_vm_disk_iops.get_vm_list()
        self.assertEqual(result, ["vm1", "vm2"])

    @patch("gather.get_vm_disk_iops.execute_cmd")
    def test_get_vm_list_failed(self, mock_exec):
        """测试获取虚机列表失败"""
        mock_exec.return_value = {
            "code": 1,
            "stdout": "",
            "stderr": "error"
        }
        result = get_vm_disk_iops.get_vm_list()
        self.assertEqual(result, [])

    # =========================
    # get_vm_disk_iops
    # =========================
    @patch("gather.get_vm_disk_iops.execute_cmd")
    def test_get_vm_disk_iops_success(self, mock_exec):
        """测试正常解析 rd_req / wr_req"""
        mock_exec.return_value = {
            "code": 0,
            "stdout": (
                "vda rd_req 100\n"
                "vda wr_req 200\n"
                "vda rd_bytes 1024\n"
            ),
            "stderr": ""
        }
        result = get_vm_disk_iops.get_vm_disk_iops("vm1")
        self.assertEqual(result["vm_name"], "vm1")
        self.assertEqual(
            len(result["disk_stats"]),
            2
        )
        metrics = [
            stat["metric"]
            for stat in result["disk_stats"]
        ]
        self.assertIn("vda", metrics[0])
        self.assertIsNotNone(result["timestamp"])

    @patch("gather.get_vm_disk_iops.execute_cmd")
    def test_get_vm_disk_iops_command_failed(self, mock_exec):
        """测试 domblkstat 执行失败"""
        mock_exec.return_value = {
            "code": 1,
            "stdout": "",
            "stderr": "virsh error"
        }
        result = get_vm_disk_iops.get_vm_disk_iops("vm1")
        self.assertEqual(
            result["error"],
            "virsh error"
        )

    @patch("gather.get_vm_disk_iops.execute_cmd")
    def test_get_vm_disk_iops_no_metrics(self, mock_exec):
        """测试没有 rd_req / wr_req"""
        mock_exec.return_value = {
            "code": 0,
            "stdout": (
                "vda rd_bytes 1024\n"
                "vda wr_bytes 2048\n"
            ),
            "stderr": ""
        }
        result = get_vm_disk_iops.get_vm_disk_iops("vm1")
        self.assertEqual(
            result["disk_stats"],
            []
        )
        self.assertIsNotNone(
            result["timestamp"]
        )

    @patch("gather.get_vm_disk_iops.execute_cmd")
    def test_get_vm_disk_iops_exception(self, mock_exec):
        """测试异常处理"""
        mock_exec.side_effect = Exception(
            "unexpected error"
        )
        result = get_vm_disk_iops.get_vm_disk_iops("vm1")
        self.assertIn(
            "error",
            result
        )

    # =========================
    # main
    # =========================
    @patch("gather.get_vm_disk_iops.get_vm_disk_iops")
    @patch("gather.get_vm_disk_iops.get_vm_list")
    @patch("builtins.print")
    def test_main(
        self,
        mock_print,
        mock_vm_list,
        mock_get_stats
    ):
        """测试 main 函数"""
        mock_vm_list.return_value = [
            "vm1"
        ]
        mock_get_stats.return_value = {
            "vm_name": "vm1",
            "disk_stats": [],
            "timestamp": "2024-01-01T00:00:00"
        }
        get_vm_disk_iops.main()
        mock_print.assert_called()

if __name__ == "__main__":
    unittest.main()
