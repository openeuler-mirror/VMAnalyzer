#!/usr/bin/env python
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
import mock
from agent import collector
from agent import vm
try:
    import libvirt
except ImportError:
    pass


class TestVMStatsCollector(unittest.TestCase):
    """
    该类用于对 `VMStatsCollector` 类进行单元测试。

    继承自 `unittest.TestCase`，主要目的是验证 `VMStatsCollector`
    类的 `record_stats` 方法是否能正确调用相关功能，
    包括通过 `libvirt` 查找虚拟机以及保存虚拟机统计信息。
    """
    @mock.patch.object(libvirt.virConnect, 'lookupByUUIDString')
    def test_record_stats(self, mock_lookup):
        vm_factory = vm.VMFactory()
        vm_info = {
            'uuid': '6717da86-fc51-474d-92fe-a76380c27c62',
            'name': 'instance-000003f9'
        }
        label = 'cpuUsage'
        vm_factory.add_vm(0, vm_info)
        vm_storage = mock.MagicMock()
        mock_save = vm_storage.save_stats_info
        vm_collector = collector.VMStatsCollector(vm_factory, vm_storage, label)
        vm_collector.record_stats()
        self.assertTrue(mock_lookup.called)
        self.assertTrue(mock_save.called)

if __name__ == '__main__':
    unittest.main()
