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
import json

from gather import get_vm_crash_status

class TestVmCrashStatus(unittest.TestCase):

    # ------------------------------
    # 测试 get_vm_list
    # ------------------------------
    @patch("gather.get_vm_crash_status.execute_cmd")
    def test_get_vm_list_success(self, mock_exec):
        mock_exec.return_value = {
            "code": 0,
            "stdout": "vm1\nvm2\n",
            "stderr": ""
        }
        result = get_vm_crash_status.get_vm_list()
        self.assertEqual(result, ["vm1", "vm2"])

    @patch("gather.get_vm_crash_status.execute_cmd")
    def test_get_vm_list_failed(self, mock_exec):
        mock_exec.return_value = {
            "code": 1,
            "stdout": "",
            "stderr": "error"
        }
        result = get_vm_crash_status.get_vm_list()
        self.assertEqual(result, [])

    # ------------------------------
    # Libvirt crashed 状态
    # ------------------------------
    @patch("gather.get_vm_crash_status.execute_cmd")
    @patch("gather.get_vm_crash_status.os.path.exists")
    def test_vm_state_crashed(self, mock_exists, mock_exec):
        mock_exists.return_value = False
        mock_exec.side_effect = [
            {"code": 0, "stdout": "crashed", "stderr": ""},
            {"code": 0, "stdout": "", "stderr": ""}
        ]
        result_json = get_vm_crash_status.get_vm_crash_status("vm1")
        result = json.loads(result_json)
