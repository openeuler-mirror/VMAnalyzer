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
import copy
from agent import analyze
from agent import vm


class VMStatsAnalyze(unittest.TestCase):
    """
    This class is used to perform unit tests on the
    virtual machine statistics analysis function.

    It inherits from unittest.TestCase and includes methods for
    initializing test data and executing test cases.
    By simulating virtual machine statistics, it verifies the correctness of
    the virtual machine statistics analysis function.
    """
    def setUp(self):
        self.vm_vcpus = 4
        self.base_stats = {
            'uuid': '6717da86-fc51-474d-92fe-a76380c27c62',
            'name': 'instance-000003f9',
            'vcpus': self.vm_vcpus,
            'cputime': 11709109249836,
            'timestamp': 1599971572
        }
        self.test_id = 168
        self.test_time = 60
        self.cpu_util = 0.2
        test_stats = copy.deepcopy(self.base_stats)
        vm_factory = vm.VMFactory()
        vm_info = {
            'uuid': test_stats['uuid'],
            'name': test_stats['name'],
            'cpu_util': self.cpu_util
        }
        vm_factory.add_vm(self.test_id, vm_info)
        # Generate simulated VM stats in 60 seconds
        self.stats_list = []
        i = 0
        while i < self.test_time:
            test_stats['cputime'] = test_stats['cputime'] + \
                100000 * test_stats['vcpus'] * int(self.cpu_util * 100)
            test_stats['timestamp'] = test_stats['timestamp'] + 1
            self.stats_list.append(copy.deepcopy(test_stats))
            i += 1

    def test_analyze(self):
        vm_factory = vm.VMFactory()
        label = 'cpuUsage'
        vm_analyze = analyze.VMStatsAnalyze(vm_factory, label)
        vm_uuid = self.base_stats['uuid']
        vm_analyzers = vm_analyze.analyze_stats(self.test_id, self.stats_list)
        for analyzers_info in vm_analyzers:
            self.assertAlmostEqual(
                 analyzers_info[self.base_stats['name']]['Current_cpu_utilization'],
                 self.cpu_util, places=5)
        self.assertAlmostEqual(vm_factory.get_vm_analyzers(self.test_id),
                               self.cpu_util, places=5)

    def test_analyze_nonexistent_vm(self):
        vm_factory = vm.VMFactory()
        label = 'cpuUsage'
        vm_analyze = analyze.VMStatsAnalyze(vm_factory, label)
        result = vm_analyze.analyze_stats(9999, self.stats_list)
        self.assertIsNone(result)

    def test_analyze_insufficient_stats(self):
        vm_factory = vm.VMFactory()
        label = 'cpuUsage'
        vm_analyze = analyze.VMStatsAnalyze(vm_factory, label)
        single_stats = [copy.deepcopy(self.base_stats)]
        result = vm_analyze.analyze_stats(self.test_id, single_stats)
        self.assertIsNone(result)

    def test_analyze_network_traffic(self):
        vm_factory = vm.VMFactory()
        label = 'networkTraffic'
        vm_analyze = analyze.VMStatsAnalyze(vm_factory, label)

        network_stats = []
        for i in range(5):
            net_stat = {
                'uuid': self.base_stats['uuid'],
                'name': self.base_stats['name'],
                'interfaceAddresses': {'eth0': '00:11:22:33:44:55'},
                'networkTraffic': {'eth0': {'rx_bytes': 1000 * (i + 1), 'tx_bytes': 500 * (i + 1)}},
                'timestamp': self.base_stats['timestamp'] + i
            }
            network_stats.append(net_stat)

        result = vm_analyze.analyze_stats(self.test_id, network_stats)
        self.assertIsNotNone(result)

    def test_analyze_memory_usage_correct_value(self):
        vm_factory = vm.VMFactory()
        label = 'memoryUsage'
        vm_analyze = analyze.VMStatsAnalyze(vm_factory, label)

        mem_stats = []
        for i in range(3):
            mem_stats.append({
                'uuid': self.base_stats['uuid'],
                'name': self.base_stats['name'],
                'totalMemory': 8192,
                'usedMemory': 4096,
                'timestamp': self.base_stats['timestamp'] + i
            })

        result = vm_analyze.analyze_stats(self.test_id, mem_stats)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        vm_name = self.base_stats['name']
        self.assertAlmostEqual(
            result[0][vm_name]['Current_mem_utilization'], 50.0, places=2)
        self.assertAlmostEqual(
            vm_factory.get_vm_analyzers(self.test_id), 50.0, places=2)

    def test_analyze_blkio_label(self):
        vm_factory = vm.VMFactory()
        label = 'blkio'
        vm_analyze = analyze.VMStatsAnalyze(vm_factory, label)

        blkio_stats = []
        for i in range(3):
            blkio_stats.append({
                'uuid': self.base_stats['uuid'],
                'name': self.base_stats['name'],
                'blkStatus': {'vda': {'capacity': 10737418240, 'allocation': 1073741824, 'physical': 1073741824}},
                'blkI/O': {'vda': {'read_bytes': 1024 * i, 'write_bytes': 512 * i,
                                   'read_requests': i, 'write_requests': i, 'errors': 0}},
                'timestamp': self.base_stats['timestamp'] + i
            })

        result = vm_analyze.analyze_stats(self.test_id, blkio_stats)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        vm_name = self.base_stats['name']
        self.assertIn('blkStatus', result[0][vm_name])
        self.assertIn('blkI/O', result[0][vm_name])

    def test_analyze_log_vm_label(self):
        vm_factory = vm.VMFactory()
        label = 'log_vm'
        vm_analyze = analyze.VMStatsAnalyze(vm_factory, label)

        log_stats = []
        for i in range(3):
            log_stats.append({
                'uuid': self.base_stats['uuid'],
                'name': self.base_stats['name'],
                'current_state': 1,
                'latest_event': 'BOOT',
                'state_log': 'log_state:running line:10 state_line:BOOT',
                'timestamp': self.base_stats['timestamp'] + i
            })

        result = vm_analyze.analyze_stats(self.test_id, log_stats)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        vm_name = self.base_stats['name']
        self.assertEqual(result[0][vm_name]['current_state'], 1)
        self.assertEqual(result[0][vm_name]['latest_event'], 'BOOT')

    def test_analyze_wrong_label_returns_empty(self):
        vm_factory = vm.VMFactory()
        vm_analyze = analyze.VMStatsAnalyze(vm_factory, 'invalidLabel')

        result = vm_analyze.analyze_stats(self.test_id, self.stats_list)
        self.assertIsNotNone(result)
        self.assertEqual(result, [])

    def test_analyze_wrong_timestamp_skipped(self):
        vm_factory = vm.VMFactory()
        label = 'cpuUsage'
        vm_analyze = analyze.VMStatsAnalyze(vm_factory, label)

        bad_stats = [
            copy.deepcopy(self.base_stats),
            {**copy.deepcopy(self.base_stats),
             'timestamp': self.base_stats['timestamp'] - 1,
             'cputime': self.base_stats['cputime'] + 1000000},
        ]
        result = vm_analyze.analyze_stats(self.test_id, bad_stats)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 0)


if __name__ == '__main__':
    unittest.main()
