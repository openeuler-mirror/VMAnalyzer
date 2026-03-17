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
import time
import subprocess
from unittest.mock import patch, MagicMock, mock_open
from gather import get_vm_basic_info as vm_monitor

class TestVMDomainMonitor(unittest.TestCase):
    """
    虚拟机基础信息采集类的单元测试
    """

    def setUp(self):
        self.monitor = vm_monitor.VMDomainMonitor()
        self.test_vm_name = "vm-test-01"
        self.test_vm_names = ["vm-test-01", "vm-test-02"]
        self.mock_domstate_running = "running"
    def tearDown(self):
        self.monitor = None

    def test_run_virsh_cmd_success(self):
        test_cmd = "virsh list --all --name"
        mock_output = "\n".join(self.test_vm_names)
        with patch("subprocess.run") as mock_subprocess:
            mock_result = MagicMock()
            mock_result.stdout.strip.return_value = mock_output
            mock_result.returncode = 0
            mock_subprocess.return_value = mock_result
            result = self.monitor.run_virsh_cmd(test_cmd)
            result = self.monitor.run_virsh_cmd(test_cmd)
            self.assertEqual(result, mock_output)
            mock_subprocess.assert_called_once_with(
                test_cmd.split(),
                capture_output=True,
                text=True,
                check=True
            )

    def test_run_virsh_cmd_fail(self):
        test_cmd = "virsh domstate non-exist-vm"
        with patch("subprocess.run") as mock_subprocess:
            mock_subprocess.side_effect = subprocess.CalledProcessError(
                returncode=1,
                cmd=test_cmd.split(),
                stderr="Domain not found"
            )
            result = self.monitor.run_virsh_cmd(test_cmd)
            self.assertIsNone(result)

    def test_get_all_vm_names(self):
        mock_output = "\n".join(self.test_vm_names)
        with patch.object(self.monitor, "run_virsh_cmd", return_value=mock_output) as mock_run_cmd:
            vm_names = self.monitor.get_all_vm_names()
            self.assertEqual(vm_names, self.test_vm_names)
            mock_run_cmd.assert_called_once_with("virsh list --all --name")

    def test_parse_domstate(self):
        with patch.object(self.monitor, "run_virsh_cmd", return_value=self.mock_domstate_running) as mock_run_cmd:
            state = self.monitor.parse_domstate(self.test_vm_name)
            self.assertEqual(state, self.mock_domstate_running)
            mock_run_cmd.assert_called_once_with(f"virsh domstate {self.test_vm_name}")
        with patch.object(self.monitor, "run_virsh_cmd", return_value=None) as mock_run_cmd:
            state = self.monitor.parse_domstate(self.test_vm_name)
            self.assertEqual(state, "unknown")

    def test_parse_domtime(self):
        with patch.object(self.monitor, "run_virsh_cmd", return_value=self.mock_domtime_output) as mock_run_cmd:
            domtime = self.monitor.parse_domtime(self.test_vm_name)
            self.assertEqual(domtime["utc_time"], "2026-02-05 10:00:00")
            self.assertEqual(domtime["local_time"], "2026-02-05 18:00:00")
            self.assertEqual(domtime["time_offset"], "28800 seconds")
            mock_run_cmd.assert_called_once_with(f"virsh domtime {self.test_vm_name}")
        with patch.object(self.monitor, "run_virsh_cmd", return_value=None):
            domtime = self.monitor.parse_domtime(self.test_vm_name)
            self.assertEqual(domtime, {})

    def test_parse_domblklist(self):
        with patch.object(self.monitor, "run_virsh_cmd", return_value=self.mock_domblklist_output):
            blk_list = self.monitor.parse_domblklist(self.test_vm_name)
            self.assertEqual(len(blk_list), 3)
            self.assertEqual(blk_list[0]["type"], "file")
            self.assertEqual(blk_list[0]["target"], "vda")
            self.assertEqual(blk_list[2]["source"], "-")

    def test_parse_domiflist_and_ifaddr(self):
        # 1. 测试parse_domiflist
        with patch.object(self.monitor, "run_virsh_cmd", return_value=self.mock_domiflist_output):
            if_list = self.monitor.parse_domiflist(self.test_vm_name)
            self.assertEqual(len(if_list), 2)
            self.assertEqual(if_list[0]["interface"], "vnet0")
            self.assertEqual(if_list[1]["mac"], "52:54:00:65:43:21")
            if_names = [iface["interface"] for iface in if_list]
            self.assertEqual(if_names, ["vnet0", "vnet1"])
        # 2. 测试parse_domifaddr
        with patch.object(self.monitor, "run_virsh_cmd", return_value=self.mock_domifaddr_output):
            if_addrs = self.monitor.parse_domifaddr(self.test_vm_name, ["vnet0", "vnet1"])
            self.assertEqual(len(if_addrs["vnet0"]), 2)
            self.assertEqual(len(if_addrs["vnet1"]), 1)
            self.assertEqual(if_addrs["vnet0"][0]["address"], "192.168.1.100/24")

    def test_parse_dommemstat_and_domstats(self):
        with patch.object(self.monitor, "run_virsh_cmd", return_value=self.mock_dommemstat_output):
            memstat = self.monitor.parse_dommemstat(self.test_vm_name)
            self.assertEqual(memstat["actual"], 2048)
            self.assertEqual(type(memstat["actual"]), int)
        with patch.object(self.monitor, "run_virsh_cmd", return_value=self.mock_domstats_output):
            domstats = self.monitor.parse_domstats(self.test_vm_name)
            self.assertEqual(domstats["cpu.time"], 12345678901234)
            self.assertNotIn("domain", domstats)

    def test_collect_single_vm_running(self):
        def mock_run_virsh_cmd(cmd):
            if "domstate" in cmd:
                return self.mock_domstate_running
            elif "domtime" in cmd:
                return self.mock_domtime_output
            elif "domblklist" in cmd:
                return self.mock_domblklist_output
            elif "domblkerror" in cmd:
                return "no_error"
            elif "domblkinfo" in cmd:
                return "Capacity: 100 GiB\nAllocation: 20 GiB\nPhysical: 20 GiB"
            elif "domiflist" in cmd:
                return self.mock_domiflist_output
            elif "domifaddr" in cmd:
                return self.mock_domifaddr_output
            elif "domif-getlink" in cmd:
                return "Link state: up"
            elif "dommemstat" in cmd:
                return self.mock_dommemstat_output
            elif "domstats" in cmd:
                return self.mock_domstats_output
            else:
                return "unknown"
        with patch.object(self.monitor, "run_virsh_cmd", side_effect=mock_run_virsh_cmd):
            vm_data = self.monitor.collect_single_vm_data(self.test_vm_name)
            self.assertEqual(vm_data["state"], "running")
            self.assertEqual(len(vm_data["block_devices"]["list"]), 3)
            self.assertEqual(len(vm_data["network_interfaces"]["list"]), 2)
            self.assertNotEqual(vm_data["memory_statistics"], {})

    def test_collect_single_vm_shutdown(self):
        with patch.object(self.monitor, "run_virsh_cmd", side_effect=lambda cmd: self.mock_domstate_shutdown if "domstate" in cmd else None):
            vm_data = self.monitor.collect_single_vm_data(self.test_vm_name)
            self.assertEqual(vm_data["state"], "shutdown")
            self.assertEqual(vm_data["network_interfaces"]["ip_addresses"], {})
            self.assertEqual(vm_data["memory_statistics"], {})

    def test_collect_all_vms(self):
        self.monitor.all_vms_data["vm_count"] = 0
        self.monitor.all_vms_data["vms"] = {}

        # 1. 测试多VM场景
        with patch.object(self.monitor, "get_all_vm_names", return_value=self.test_vm_names):
            mock_vm_data = {"name": self.test_vm_name, "state": "running"}
            with patch.object(self.monitor, "collect_single_vm_data", return_value=mock_vm_data):
                self.monitor.collect_all_vms()
                self.assertEqual(self.monitor.all_vms_data["vm_count"], 2)
                self.assertIn("vm-test-01", self.monitor.all_vms_data["vms"])
                self.assertIn("vm-test-02", self.monitor.all_vms_data["vms"])

        # 2. 测试无VM场景（关键：重置后再测试）
        self.monitor.all_vms_data["vm_count"] = 0
        self.monitor.all_vms_data["vms"] = {}
        with patch.object(self.monitor, "get_all_vm_names", return_value=[]):
            self.monitor.collect_all_vms()
            self.assertEqual(self.monitor.all_vms_data["vm_count"], 0)
            self.assertEqual(self.monitor.all_vms_data["vms"], {})

    def test_save_to_json(self):
        self.monitor.all_vms_data["vm_count"] = 1
        self.monitor.all_vms_data["vms"][self.test_vm_name] = {"state": "running"}
        test_file_path = "test_vm_monitor.json"

        # 1.测试指定文件路径
        with patch("builtins.open", mock_open()) as mock_file:
            self.monitor.save_to_json(test_file_path)
            mock_file.assert_called_once_with(test_file_path, "w", encoding="utf-8")
            # 单独mock json.dump，避免作用域干扰
            with patch("json.dump") as mock_json_dump:
                self.monitor.save_to_json(test_file_path)
                mock_json_dump.assert_called_once()

        # 2.测试默认文件名：独立Mock块，避免复用之前的mock_file
        with patch("builtins.open", mock_open()) as mock_default_file:
            self.monitor.save_to_json()  # 不传入路径，使用默认名
            # 断言默认文件名包含指定前缀
            call_args = mock_default_file.call_args[0][0]
            self.assertIn("vm_domain_monitor_", call_args)
            # 断言文件打开模式正确
            mock_default_file.assert_called_once_with(call_args, "w", encoding="utf-8")

if __name__ == "__main__":
    unittest.main(verbosity=2)
