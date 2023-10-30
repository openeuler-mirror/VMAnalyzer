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
import mock
from agent import reporter
from agent import vm


class TestVMAnalyzersReporter(unittest.TestCase):
    def setUp(self):
        self.test_vm = {
            'uuid': '6717da86-fc51-474d-92fe-a76380c27c62',
            'name': 'instance-000003f9'
        }
        self.test_id = 168

    def test_startReport(self):
        vm_factory = vm.VMFactory()
        vm_storage = mock.MagicMock()
        vm_analyzer = mock.MagicMock()
        vm_viewer = mock.MagicMock()
        mock_stat = vm_storage.getStatsInfo
        mock_analyzer = vm_analyzer.analyzeStats
        mock_output = vm_viewer.output
        vm_factory.addVM(self.test_id, self.test_vm)
        vm_reporter = reporter.VMAnalyzersReporter(vm_factory, vm_storage, vm_viewer, vm_analyzer)
        vm_reporter.startReport()
        self.assertEqual(mock_stat.called, True)
        self.assertEqual(mock_analyzer.called, True)
        self.assertEqual(mock_output.called, True)

if __name__ == "__main__":
        unittest.main()
