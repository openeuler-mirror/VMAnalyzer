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
import libvirt

import gather.get_vm_schedu_info as get_vm_schedu_info

class TestGetVMScheduInfo(unittest.TestCase):
    @patch("get_vm_schedu_info.open", new_callable=mock_open)
    @patch("get_vm_schedu_info.libvirt.open")
    def test_main_success(self, mock_libvirt_open, mock_file):
        """测试正常流程：存在运行虚机和关闭虚机"""
        # mock connection
        mock_conn = MagicMock()
        mock_libvirt_open.return_value = mock_conn
        # 运行虚机
        mock_conn.listDomainsID.return_value = [1]
        running_dom = MagicMock()
        running_dom.name.return_value = "vm_running"
        running_dom.schedulerType.return_value = "posix"
        running_dom.schedulerParameters.return_value = {"cpu_shares": 1024}
        running_dom.jobInfo.return_value = (1, 0, 100, 200)
        running_dom.ioThreadInfo.return_value = [(1, {0, 1})]
        mock_conn.lookupByID.return_value = running_dom
        # 关闭虚机
        mock_conn.listDefinedDomains.return_value = ["vm_stop"]
        stop_dom = MagicMock()
        stop_dom.name.return_value = "vm_stop"
        stop_dom.schedulerType.return_value = "posix"
        stop_dom.schedulerParameters.return_value = {"cpu_shares": 512}
        stop_dom.jobInfo.side_effect = libvirt.libvirtError("no job")
        stop_dom.ioThreadInfo.return_value = []
        mock_conn.lookupByName.return_value = stop_dom
        get_vm_schedu_info.main()
        # 检查文件是否写入
        mock_file.assert_called_once_with(
            "vm_scheduler_info.json", "w", encoding="utf-8"
        )
        handle = mock_file()
        written = "".join(call.args[0] for call in handle.write.call_args_list)
        result = json.loads(written)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "vm_running")
        self.assertEqual(result[1]["name"], "vm_stop")
        mock_conn.close.assert_called_once()

    @patch("get_vm_schedu_info.libvirt.open")
    def test_libvirt_connect_fail(self, mock_open):
        """测试 libvirt 连接失败"""
        mock_open.return_value = None
        with patch("builtins.print") as mock_print:
            get_vm_schedu_info.main()
        mock_print.assert_any_call("无法连接到 libvirt 守护进程！")

    @patch("get_vm_schedu_info.open", new_callable=mock_open)
    @patch("get_vm_schedu_info.libvirt.open")
    def test_jobinfo_exception(self, mock_libvirt_open, mock_file):
        """测试 jobInfo 抛异常"""
        mock_conn = MagicMock()
        mock_libvirt_open.return_value = mock_conn
        mock_conn.listDomainsID.return_value = [1]
        mock_conn.listDefinedDomains.return_value = []
        dom = MagicMock()
        dom.name.return_value = "vm1"
        dom.schedulerType.return_value = "posix"
        dom.schedulerParameters.return_value = {}
        dom.jobInfo.side_effect = libvirt.libvirtError("no job")
        dom.ioThreadInfo.return_value = []
        mock_conn.lookupByID.return_value = dom
        get_vm_schedu_info.main()
        mock_conn.close.assert_called_once()

    @patch("get_vm_schedu_info.open", new_callable=mock_open)
    @patch("get_vm_schedu_info.libvirt.open")
    def test_iothread_exception(self, mock_libvirt_open, mock_file):
        """测试 ioThreadInfo 抛异常"""
        mock_conn = MagicMock()
        mock_libvirt_open.return_value = mock_conn
        mock_conn.listDomainsID.return_value = [1]
        mock_conn.listDefinedDomains.return_value = []
        dom = MagicMock()
        dom.name.return_value = "vm1"
        dom.schedulerType.return_value = "posix"
        dom.schedulerParameters.return_value = {}
        dom.jobInfo.return_value = (1, 0, 0, 0)
        dom.ioThreadInfo.side_effect = libvirt.libvirtError("error")
        mock_conn.lookupByID.return_value = dom
        get_vm_schedu_info.main()
        mock_conn.close.assert_called_once()

if __name__ == "__main__":
    unittest.main()
