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
import os
import json
import shutil
import subprocess
from datetime import datetime
from unittest.mock import patch, MagicMock

from gather.get_vm_load_and_lastboot import VMSysMonitor, logger

class TestGetVMLoadAndLastboot(unittest.TestCase):
    """VM负载和最后启动时间采集模块单测"""
    def setUp(self):
        self.poll_interval = 1
        test_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.test_out_dir = os.path.join(test_root, "temp", "test_vm_load_lastboot")

        class TestableVMSysMonitor(VMSysMonitor):
            def call_run_cmd(self, cmd):
                return super()._run_cmd(cmd)

        self.monitor = TestableVMSysMonitor(poll=self.poll_interval, out_dir=self.test_out_dir)

    def tearDown(self):
        test_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        temp_dir = os.path.join(test_root, "temp")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

    def test__run_cmd_success(self):
        test_cmd = "virsh list --name"
        mock_stdout = "node-vm01 node-vm02"
        with patch("subprocess.run") as mock_subproc:
            mock_res = MagicMock()
            mock_res.stdout.strip.return_value = mock_stdout
            mock_subproc.return_value = mock_res
            result = self.monitor.call_run_cmd(test_cmd)
            self.assertEqual(result, mock_stdout)
            mock_subproc.assert_called_once_with(
                test_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                universal_newlines=True, check=True, timeout=30
            )

    def test__run_cmd_called_process_error(self):
        test_cmd = "virsh list --name"
        with patch("subprocess.run") as mock_subproc, patch.object(logger, "error") as mock_log_err:
            # 场景1：错误含not supported/unknown command，不打印错误日志
            mock_subproc.side_effect = subprocess.CalledProcessError(
                returncode=1, cmd=test_cmd, stderr="operation not supported"
            )
            self.assertIsNone(self.monitor.call_run_cmd(test_cmd))
            mock_log_err.assert_not_called()

            # 场景2：其他错误，打印错误日志
            mock_subproc.side_effect = subprocess.CalledProcessError(
                returncode=1, cmd=test_cmd, stderr="failed to connect to libvirt"
            )
            self.assertIsNone(self.monitor.call_run_cmd(test_cmd))
            mock_log_err.assert_called_once()

    def test__run_cmd_other_exceptions(self):
        test_cmd = "virsh list --name"
        with patch("subprocess.run") as mock_subproc, patch.object(logger, "error") as mock_log_err:
            # 场景1：超时异常
            mock_subproc.side_effect = subprocess.TimeoutExpired(cmd=test_cmd, timeout=30)
            self.assertIsNone(self.monitor.call_run_cmd(test_cmd))
            mock_log_err.assert_called_once()

            # 场景2：通用异常，先重置mock，再调用方法
            mock_subproc.side_effect = Exception("system error")
            mock_log_err.reset_mock()
            self.assertIsNone(self.monitor.call_run_cmd(test_cmd))
            mock_log_err.assert_called_once()

    def test_get_running_vms(self):
        # 场景1：有运行的VM，返回非空列表
        with patch.object(self.monitor, "_run_cmd") as mock_run_cmd:
            mock_run_cmd.return_value = "vm-web01 vm-db01"
            vms = self.monitor.get_running_vms()
            self.assertEqual(vms, ["vm-web01", "vm-db01"])
            mock_run_cmd.assert_called_once_with("virsh list --name | grep -v '^$'")

        with patch.object(self.monitor, "_run_cmd") as mock_run_cmd:
            mock_run_cmd.return_value = None
            self.assertEqual(self.monitor.get_running_vms(), [])

if __name__ == "__main__":
    unittest.main(verbosity=2)
