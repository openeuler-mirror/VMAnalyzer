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
import logging

class VMStatsAnalyze(object):
    """
    The `VMStatsAnalyze` class is used to analyze the statistical
    information of virtual machines.

    This class analyzes the statistical information of virtual machines
    according to the specified label (such as CPU usage, memory usage, etc.),
    stores the analysis results in the virtual machine factory,
    and returns a list of analysis results.
    """
    def __init__(self, vm_factory, label):
        self.__vm_factory = vm_factory
        self.__label = label

    def analyze_stats(self, vm_id, vm_stats_info):

        vm_factory = self.__vm_factory
        label = self.__label

        if vm_id not in vm_factory.vms:
            return
        vm_info = vm_factory.get_vm(vm_id)
        if len(vm_stats_info) < 2:
            logging.warning('There are too less stats of VM: %s',
                            vm_info['name'])
            return

        analyzers_list = []
        logging.debug('Length of VM stats: %d', len(vm_stats_info))

        if label == 'cpuUsage':

            for i in range(len(vm_stats_info) - 1):
                assert vm_stats_info[i]['uuid'] == vm_stats_info[i+1]['uuid']
                # User can adjust the number of vcpus???
                vcpu_count = vm_stats_info[i]['vcpus']
                logging.debug('VM %s: previous cputime: %ld, '
                              'latter cputime: %ld, '
                              'previous timestamp: %d, latter timestamp: %d',
                              vm_info['name'], vm_stats_info[i]['cputime'],
                              vm_stats_info[i+1]['cputime'],
                              vm_stats_info[i]['timestamp'],
                              vm_stats_info[i+1]['timestamp'])

                # Calculate cpu utilization:
                # %cpu = 100 × cpu_time_diff / (t × nr_cores × 10^9)
                delta_cputime = int(vm_stats_info[i+1]['cputime']) \
                                - int(vm_stats_info[i]['cputime'])
                delta_timestamp = vm_stats_info[i+1]['timestamp'] \
                                  - vm_stats_info[i]['timestamp']
                # We don't want wrong timestamp
                if delta_timestamp <= 0:
                    logging.warning('We got wrong timestamp of VM: %s',
                                    vm_info['name'])
                    continue
                cpu_util = delta_cputime * 100.0 \
                           / (delta_timestamp * vcpu_count * 1e9)

                logging.debug('VM %s: vcpu count: %d, cpu utilization: %.2f%%',
                              vm_info['name'], vcpu_count, cpu_util * 100)

                # FIXME, whether to keep 2 decimal digits
                analyzers_info = {
                    'Current_cpu_utilization': round(cpu_util, 4),
                    'TimeStamp': vm_stats_info[i + 1]['timestamp']
                }
                analyzers_list.append({vm_info['name']: analyzers_info})
            # store VM analyzers in DB
            vm_factory.set_vm_analyzers(vm_id, round(cpu_util, 4))

        elif label == 'memoryUsage':

            for i in range(len(vm_stats_info) - 1):
                assert vm_stats_info[i]['uuid'] == vm_stats_info[i+1]['uuid']

                # Calculate Memory utilization: (usedMemory / totalMemory) * 100
                mem_util = (int(vm_stats_info[i]['usedMemory']) /
                            int(vm_stats_info[i]['totalMemory'])) * 100

                logging.debug('VM %s: memory utilization: %.2f%%',
                              vm_info['name'], mem_util)
                analyzers_info = {
                    'Current_mem_utilization': round(mem_util, 4),
                    'TimeStamp': vm_stats_info[i + 1]['timestamp']
                }
                analyzers_list.append({vm_info['name']: analyzers_info})
            # store VM analyzers in DB
            vm_factory.set_vm_analyzers(vm_id, round(mem_util, 4))

        elif label == 'networkTraffic':

            for i in range(len(vm_stats_info) - 1):
                assert vm_stats_info[i]['uuid'] == vm_stats_info[i+1]['uuid']

                analyzers_info = {
                    'interfaceAddresses': \
                        vm_stats_info[i]['interfaceAddresses'],
                    'networkTraffic': vm_stats_info[i]['networkTraffic'],
                    'TimeStamp': vm_stats_info[i + 1]['timestamp']
                 }
                analyzers_list.append({vm_info['name']: analyzers_info})

        elif label == 'blkio':
            for i in range(len(vm_stats_info) - 1):
                assert vm_stats_info[i]['uuid'] == vm_stats_info[i+1]['uuid']

                analyzers_info = {
                    'blkStatus': vm_stats_info[i]['blkStatus'],
                    'blkI/O': vm_stats_info[i]['blkI/O'],
                    'TimeStamp': vm_stats_info[i + 1]['timestamp']
                }
                analyzers_list.append({vm_info['name']: analyzers_info})

        elif label == 'log_vm':
            for i in range(len(vm_stats_info) - 1):
                assert vm_stats_info[i]['uuid'] == vm_stats_info[i+1]['uuid']

                analyzers_info = {
                    'current_state': vm_stats_info[i]['current_state'],
                    'latest_event': vm_stats_info[i]['latest_event'],
                    'state_log': vm_stats_info[i]['state_log'],
                    'TimeStamp': vm_stats_info[i + 1]['timestamp']
                }
                analyzers_list.append({vm_info['name']: analyzers_info})

        else:
            logging.error('wrong label!')

        return analyzers_list
