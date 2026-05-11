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
from agent import vm


class TestVMFactory(unittest.TestCase):
    """
    该类用于对 `VMFactory` 类进行单元测试。

    继承自 `unittest.TestCase`，包含多个测试方法，用于验证 `VMFactory` 类的各个功能，
    如获取连接、添加虚拟机、获取虚拟机信息、删除虚拟机以及设置虚拟机分析器信息等。
    """
    def setUp(self):
        self.test_vm = {
            'uuid': '6717da86-fc51-474d-92fe-a76380c27c62',
            'name': 'instance-000003f9'
        }
        self.test_id = 168
        self.test_score = 300

    def test_vc(self):
        vm_factory = vm.VMFactory()
        vc = vm_factory.vc
        self.assertTrue(vc.isAlive())

    def test_add_vm(self):
        vm_factory = vm.VMFactory()
        vm_factory.add_vm(self.test_id, self.test_vm)
        self.assertDictEqual(vm_factory.vms[self.test_id], self.test_vm)
        vm_factory = vm.VMFactory()
        self.assertDictEqual(vm_factory.vms[self.test_id], self.test_vm)
        vm_factory.del_vm(self.test_id)

    def test_get_vm(self):
        vm_factory = vm.VMFactory()
        vm_factory.add_vm(self.test_id, self.test_vm)
        self.assertDictEqual(vm_factory.get_vm(self.test_id), self.test_vm)
        vm_factory.del_vm(self.test_id)

    def test_del_vm(self):
        vm_factory = vm.VMFactory()
        vm_factory.add_vm(self.test_id, self.test_vm)
        vm_factory.del_vm(self.test_id)
        self.assertEqual(vm_factory.vms, {})

    def test_set_vm_analyzers(self):
        vm_factory = vm.VMFactory()
        vm_factory.add_vm(self.test_id, self.test_vm)
        vm_factory.set_vm_analyzers(self.test_id, self.test_score)
        self.assertEqual(vm_factory.get_vm_analyzers(self.test_id),
                         self.test_score)

if __name__ == '__main__':
    unittest.main()
