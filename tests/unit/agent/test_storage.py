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
import random
import copy
from agent import storage
import mock
from agent import vm


class TestVMStatsRedisStorage(unittest.TestCase):
    def setUp(self):
        self.test_vm = {
            'uuid': '6717da86-fc51-474d-92fe-a76380c27c62',
            'name': 'instance-000003f9',
            'cpu_util': 0.2
        }
        self.test_id = 168
        vm_factory = vm.VMFactory()
        vm_factory.addVM(self.test_id, self.test_vm)
        self.vm_factory = vm_factory
        self.base_stats = {
            'uuid': self.test_vm['uuid'],
            'name': self.test_vm['name'],
            'vcpus': 4,
            'cputime': 11709109249836,
            'timestamp': 1599971572
        }
        test_stats = copy.deepcopy(self.base_stats)
        self.start_time = test_stats['timestamp']
        # Generate simulated VM stats in 60 seconds
        self.stats_list = []
        self.test_time = 60
        for i in range(self.test_time):
            test_stats['cputime'] = test_stats['cputime'] + random.randint(1, 50)
            test_stats['timestamp'] = test_stats['timestamp'] + 1
            self.stats_list.append(copy.deepcopy(test_stats))
        self.end_time = test_stats['timestamp']

    def test_saveStatsInfo(self):
        vm_storage = storage.VMStatsRedisStorage(self.vm_factory)
        for stats in self.stats_list:
            vm_storage.saveStatsInfo({self.test_id: stats})
        self.assertEqual(vm_storage.sr.zcount(self.test_vm['uuid'], self.start_time, self.end_time), self.test_time)
        vm_storage.sr.zremrangebyscore(self.test_vm['uuid'], self.start_time, self.end_time)

    def test_getStatsInfo(self):
        vm_storage = storage.VMStatsRedisStorage(self.vm_factory)
        for vm_stats in self.stats_list:
            vm_storage.saveStatsInfo({self.test_id: vm_stats})
        vm_stats = vm_storage.getStatsInfo(self.test_id, self.start_time, self.end_time)
        self.assertEqual(len(vm_stats), self.test_time)
        count = 0
        for stats in self.stats_list:
            self.assertDictEqual(vm_stats[count], stats)
            count = count + 1
        vm_storage.sr.zremrangebyscore(self.test_vm['uuid'], self.start_time, self.end_time)

if __name__ == "__main__":
        unittest.main()
