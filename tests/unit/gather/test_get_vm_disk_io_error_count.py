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
from unittest.mock import patch, MagicMock
import subprocess
import json

from gather import get_vm_disk_io_error_count

class TestGetVmDiskIoErrorCount(unittest.TestCase):

    # =========================
    # execute_cmd
    # =========================
    @patch("gather.get_vm_disk_io_error_count.subprocess.run")
    def test_execute_cmd_success(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="ok\n",
            stderr=""
        )
        result = ( 
            get_vm_disk_io_error_count
            .execute_cmd(["cmd"])
        )
        self.assertEqual(result["code"], 0)
        self.assertEqual(result["stdout"], "ok")

    @patch("gather.get_vm_disk_io_error_count.subprocess.run")
    def test_execute_cmd_timeout(self, mock_run):
        mock_run.side_effect = subprocess.TimeoutExpired(
            cmd="cmd",
            timeout=30
        )
        result = (
            get_vm_disk_io_error_count
            .execute_cmd(["cmd"])
        )
        self.assertEqual(result["code"], -1)
        self.assertIn("超时", result["stderr"])

    @patch("gather.get_vm_disk_io_error_count.subprocess.run")
    def test_execute_cmd_exception(self, mock_run):
        mock_run.side_effect = Exception("boom")
        result = (
            get_vm_disk_io_error_count
            .execute_cmd(["cmd"])
        )
        self.assertEqual(result["code"], -1)
        self.assertIn("异常", result["stderr"])

    # =========================
    # get_vm_disk_list
    # =========================
    @patch(
        "gather.get_vm_disk_io_error_count.execute_cmd"
    )
    def test_get_vm_disk_list_success(
        self,
        mock_exec
    ):
        stdout = (
            "Type Device Target Source\n"
            "---------------------------------------\n"
            "file disk vda /path/disk1\n"
            "file disk vdb /path/disk2\n"
        )
        mock_exec.return_value = {
            "code": 0,
            "stdout": stdout,
            "stderr": ""
        }
        result = (
            get_vm_disk_io_error_count
            .get_vm_disk_list("vm1")
        )
        self.assertEqual(len(result), 2)
        self.assertEqual(
            result[0]["target"],
            "vda"
        )

    @patch(
        "gather.get_vm_disk_io_error_count.execute_cmd"
    )
    def test_get_vm_disk_list_fail(
        self,
        mock_exec
    ):
        mock_exec.return_value = {
            "code": 1,
            "stdout": "",
            "stderr": "error"
        }
        result = (
            get_vm_disk_io_error_count
            .get_vm_disk_list("vm1")
        )
        self.assertEqual(result, [])

    # =========================
    # get_vm_list
    # =========================
    @patch(
        "gather.get_vm_disk_io_error_count.execute_cmd"
    )
    def test_get_vm_list_success(
        self,
        mock_exec
    ):
        mock_exec.return_value = {
            "code": 0,
            "stdout": "vm1\nvm2\n",
            "stderr": ""
        }
        result = (
            get_vm_disk_io_error_count
            .get_vm_list()
        )
        self.assertEqual(
            result,
            ["vm1", "vm2"]
        )

    @patch(
        "gather.get_vm_disk_io_error_count.execute_cmd"
    )
    def test_get_vm_list_fail(
        self,
        mock_exec
    ):
        mock_exec.return_value = {
            "code": 1,
            "stdout": "",
            "stderr": "error"
        }
        result = (
            get_vm_disk_io_error_count
            .get_vm_list()
        )
        self.assertEqual(result, [])

    # =========================
    # get_vm_disk_io_error_count
    # =========================
    @patch(
        "gather.get_vm_disk_io_error_count.execute_cmd"
    )
    @patch(
        "gather.get_vm_disk_io_error_count.get_vm_disk_list"
    )
    def test_get_vm_disk_io_error_count_success(
        self,
        mock_get_disks,
        mock_exec
    ):
        mock_get_disks.return_value = [
            {"target": "vda"},
            {"target": "vdb"}
        ]
        blk_stdout = (
            "Read errors: 1\n"
            "Write errors: 2\n"
            "Flush errors: 3\n"
        )
        mock_exec.return_value = {
            "code": 0,
            "stdout": blk_stdout,
            "stderr": ""
        }
        result_json = (
            get_vm_disk_io_error_count
            .get_vm_disk_io_error_count("vm1")
        )
        result = json.loads(result_json)
        self.assertTrue(result["success"])
        self.assertEqual(
            result["disks"][0]["read_errors"],
            1
        )
        self.assertEqual(
            result["disks"][0]["write_errors"],
            2
        )
        self.assertEqual(
            result["disks"][0]["flush_errors"],
            3
        )

    @patch(
        "gather.get_vm_disk_io_error_count.get_vm_disk_list"
    )
    def test_get_vm_disk_io_error_count_no_disks(
        self,
        mock_get_disks
    ):
        mock_get_disks.return_value = []
        result_json = (
            get_vm_disk_io_error_count
            .get_vm_disk_io_error_count("vm1")
        )
        result = json.loads(result_json)
        self.assertFalse(result["success"])
        self.assertIn(
            "未获取到虚机磁盘列表",
            result["error"]
        )

    @patch(
        "gather.get_vm_disk_io_error_count.execute_cmd"
    )
    @patch(
        "gather.get_vm_disk_io_error_count.get_vm_disk_list"
    )
    def test_get_vm_disk_io_error_count_domblkerror_fail(
        self,
        mock_get_disks,
        mock_exec
    ):
        mock_get_disks.return_value = [
            {"target": "vda"}
        ]
        mock_exec.return_value = {
            "code": 1,
            "stdout": "",
            "stderr": "permission denied"
        }
        result_json = (
            get_vm_disk_io_error_count
            .get_vm_disk_io_error_count("vm1")
        )
        result = json.loads(result_json)
        self.assertIn(
            "domblkerror命令执行失败",
            result["disks"][0]["blk_error"]
        )

    @patch(
        "gather.get_vm_disk_io_error_count.execute_cmd"
    )
    @patch(
        "gather.get_vm_disk_io_error_count.get_vm_disk_list"
    )
    def test_get_vm_disk_io_error_count_parse_error(
        self,
        mock_get_disks,
        mock_exec
    ):
        mock_get_disks.return_value = [
            {"target": "vda"}
        ]
        blk_stdout = (
            "Read errors: abc\n"
            "Write errors: xyz\n"
            "Flush errors: ???\n"
        )
        mock_exec.return_value = {
            "code": 0,
            "stdout": blk_stdout,
            "stderr": ""
        }
        result_json = (
            get_vm_disk_io_error_count
            .get_vm_disk_io_error_count("vm1")
        )
        result = json.loads(result_json)
        self.assertEqual(
            result["disks"][0]["read_errors"],
            0
        )
        self.assertEqual(
            result["disks"][0]["write_errors"],
            0
        )
        self.assertEqual(
            result["disks"][0]["flush_errors"],
            0
        )

if __name__ == "__main__":
    unittest.main()
