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

if __name__ == "__main__":
    unittest.main()
