#!/usr/bin/env python
# _*_coding: utf-8 _*_
#######################################################################################
# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#          http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.
#######################################################################################
import unittest
from agent import vm


class TestVMFactory(unittest.TestCase):
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

    def test_addVM(self):
        vm_factory = vm.VMFactory()
        vm_factory.addVM(self.test_id, self.test_vm)
        self.assertDictEqual(vm_factory.vms[self.test_id], self.test_vm)
        vm_factory = vm.VMFactory()
        self.assertDictEqual(vm_factory.vms[self.test_id], self.test_vm)
        vm_factory.delVM(self.test_id)

    def test_getVM(self):
        vm_factory = vm.VMFactory()
        vm_factory.addVM(self.test_id, self.test_vm)
        self.assertDictEqual(vm_factory.getVM(self.test_id), self.test_vm)
        vm_factory.delVM(self.test_id)

    def test_delVM(self):
        vm_factory = vm.VMFactory()
        vm_factory.addVM(self.test_id, self.test_vm)
        vm_factory.delVM(self.test_id)
        self.assertEqual(vm_factory.vms, {})

    def test_setAnalyzersVM(self):
        vm_factory = vm.VMFactory()
        vm_factory.addVM(self.test_id, self.test_vm)
        vm_factory.setVMAnalyzers(self.test_id, self.test_score)
        self.assertEqual(vm_factory.getVMAnalyzers(self.test_id), self.test_score)

if __name__ == "__main__":
        unittest.main()
