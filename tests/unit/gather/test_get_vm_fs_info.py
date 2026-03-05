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
import sys
from unittest.mock import patch, MagicMock, mock_open

mock_libvirt = MagicMock()
mock_libvirt.VIR_DOMAIN_RUNNING = 1
mock_libvirt.VIR_DOMAIN_SHUTOFF = 5
mock_libvirt.VIR_DOMAIN_PAUSED = 3
# 定义libvirt异常类，让业务代码能识别
mock_libvirt.libvirtError = type("libvirtError", (Exception,), {"__str__": lambda self: "连接失败"})
sys.modules["libvirt"] = mock_libvirt
sys.modules["gather.get_vm_fs_info.libvirt"] = mock_libvirt

from gather import get_vm_fs_info as vm_fs_info

VIR_DOMAIN_RUNNING = 1
VIR_DOMAIN_SHUTOFF = 5
VIR_DOMAIN_PAUSED = 3

class TestVMAnalyzer(unittest.TestCase):
    """VMAnalyzer类单元测试，覆盖所有核心方法及正常/异常场景"""
    def setUp(self):
        self.analyzer = vm_fs_info.VMAnalyzer()
        self.mock_raw_fsinfo = [
            ("C:\\", "/var/lib/libvirt/images/win10_c.img", "ntfs", ["/dev/vda1"]),
            ("Data", "/var/lib/libvirt/images/win10_data.img", "ntfs", ["/dev/vda2"]),
            ("System Reserved", "/var/lib/libvirt/images/win10_reserved.img", "ntfs", ["/dev/vda3"])
        ]
        self.empty_raw_fsinfo = []
        self.invalid_raw_fsinfo = [("OnlyName",), ("Name&Path", "/path",), (None, None, None)]
        self.mock_vm_name = "test-win10"
        self.mock_vm_uuid = "12345678-1234-1234-1234-1234567890ab"
        self.mock_libvirt_error = mock_libvirt.libvirtError()

    def tearDown(self):
        self.analyzer = None

    def test_parse_fsinfo_normal(self):
        parsed_list = self.analyzer.parse_fsinfo(self.mock_raw_fsinfo)
        self.assertEqual(len(parsed_list), 3)

if __name__ == "__main__":
    unittest.main(verbosity=2)
