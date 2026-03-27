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
import logging
from utils import config

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
            return []
        vm_info = vm_factory.get_vm(vm_id)
        if len(vm_stats_info) < 2:
            logging.warning('There are too less stats of VM: %s',
                            vm_info['name'])
            return []

        analyzers_list = []
        logging.debug('Length of VM stats: %d', len(vm_stats_info))

        if label == 'cpuUsage':
            cpu_utils = []
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
                # cpu_util is already a percentage (0–100); do not multiply again
                logging.debug('VM %s: vcpu count: %d, cpu utilization: %.4f%%',vm_info['name'], vcpu_count, cpu_util)

                cpu_utils.append(cpu_util)
                # FIXME, whether to keep 2 decimal digits
                analyzers_info = {
                    'Current_cpu_utilization': round(cpu_util, 4),
                    'TimeStamp': vm_stats_info[i + 1]['timestamp']
                }
                analyzers_list.append({vm_info['name']: analyzers_info})
            # store VM analyzers in DB
            #vm_factory.set_vm_analyzers(vm_id, round(cpu_util, 4))
            if cpu_utils:
                vm_factory.set_vm_analyzers(vm_id, round(cpu_utils[-1], 4))


                summary_info = {
                    'min_cpu_utilization': round(min(cpu_utils), 4),
                    'max_cpu_utilization': round(max(cpu_utils), 4),
                    'avg_cpu_utilization': round(sum(cpu_utils) / len(cpu_utils), 4),
                }
                analyzers_list.append({vm_info['name'] + '_summary': summary_info})

                threshold = config.ALERT_THRESHOLDS.get('cpu_usage', 90.0)
                if cpu_utils[-1] > threshold:
                    logging.warning(
                        'ALERT: VM %s CPU usage %.2f%% exceeds threshold %.2f%%',
                        vm_info['name'], cpu_utils[-1], threshold)

        elif label == 'memoryUsage':

            mem_utils = []
            for i in range(len(vm_stats_info) - 1):
                assert vm_stats_info[i]['uuid'] == vm_stats_info[i+1]['uuid']

                # Calculate Memory utilization from the newer (i+1) sample so
                # that the value and the timestamp are consistent.
                mem_util = (int(vm_stats_info[i+1]['usedMemory']) /
                            int(vm_stats_info[i+1]['totalMemory'])) * 100

                logging.debug('VM %s: memory utilization: %.2f%%',
                              vm_info['name'], mem_util)

                mem_utils.append(mem_util)
                analyzers_info = {
                    'Current_mem_utilization': round(mem_util, 4),
                    'TimeStamp': vm_stats_info[i + 1]['timestamp']
                }
                analyzers_list.append({vm_info['name']: analyzers_info})
            # store VM analyzers in DB
            #vm_factory.set_vm_analyzers(vm_id, round(mem_util, 4))
            if mem_utils:
                vm_factory.set_vm_analyzers(vm_id, round(mem_utils[-1], 4))

                summary_info = {
                    'min_mem_utilization': round(min(mem_utils), 4),
                    'max_mem_utilization': round(max(mem_utils), 4),
                    'avg_mem_utilization': round(sum(mem_utils) / len(mem_utils), 4),
                }
                analyzers_list.append({vm_info['name'] + '_summary': summary_info})

                threshold = config.ALERT_THRESHOLDS.get('memory_usage', 85.0)
                if mem_utils[-1] > threshold:
                    logging.warning(
                        'ALERT: VM %s memory usage %.2f%% exceeds threshold %.2f%%',
                        vm_info['name'], mem_utils[-1], threshold)

        elif label == 'networkTraffic':

            for i in range(len(vm_stats_info) - 1):
                assert vm_stats_info[i]['uuid'] == vm_stats_info[i+1]['uuid']
                delta_timestamp = (vm_stats_info[i+1]['timestamp']
                                   - vm_stats_info[i]['timestamp'])
         
                traffic_rate = {}
                prev_traffic = vm_stats_info[i]['networkTraffic']
                curr_traffic = vm_stats_info[i+1]['networkTraffic']
                if (delta_timestamp > 0
                        and isinstance(prev_traffic, dict)
                        and isinstance(curr_traffic, dict)):
                    for iface, prev in prev_traffic.items():
                        if iface in curr_traffic:
                            curr = curr_traffic[iface]
                            traffic_rate[iface] = {
                                'rx_bytes_rate':   round((curr['rx_bytes']   - prev['rx_bytes'])   / delta_timestamp, 2),
                                'tx_bytes_rate':   round((curr['tx_bytes']   - prev['tx_bytes'])   / delta_timestamp, 2),
                                'rx_packets_rate': round((curr['rx_packets'] - prev['rx_packets']) / delta_timestamp, 2),
                                'tx_packets_rate': round((curr['tx_packets'] - prev['tx_packets']) / delta_timestamp, 2),
                            }

                analyzers_info = {
                    'interfaceAddresses': vm_stats_info[i]['interfaceAddresses'],
                    'networkTraffic_rate': traffic_rate,
                    'TimeStamp': vm_stats_info[i + 1]['timestamp']
                }
                analyzers_list.append({vm_info['name']: analyzers_info})

        elif label == 'blkio':
            for i in range(len(vm_stats_info) - 1):
                assert vm_stats_info[i]['uuid'] == vm_stats_info[i+1]['uuid']
                delta_timestamp = (vm_stats_info[i+1]['timestamp']
                                   - vm_stats_info[i]['timestamp'])

                io_rate = {}
                prev_io = vm_stats_info[i]['blkI/O']
                curr_io = vm_stats_info[i+1]['blkI/O']
                if (delta_timestamp > 0
                        and isinstance(prev_io, dict)
                        and isinstance(curr_io, dict)):
                    for dev, prev in prev_io.items():
                        if dev in curr_io:
                            curr = curr_io[dev]
                            io_rate[dev] = {
                                'read_bytes_rate':    round((curr['read_bytes']    - prev['read_bytes'])    / delta_timestamp, 2),
                                'write_bytes_rate':   round((curr['write_bytes']   - prev['write_bytes'])   / delta_timestamp, 2),
                                'read_requests_rate': round((curr['read_requests'] - prev['read_requests']) / delta_timestamp, 2),
                                'write_requests_rate':round((curr['write_requests']- prev['write_requests'])/ delta_timestamp, 2),
                            }

                analyzers_info = {
                    'blkStatus': vm_stats_info[i]['blkStatus'],
                    'blkI/O_rate': io_rate,
                    'TimeStamp': vm_stats_info[i + 1]['timestamp']
                }
                analyzers_list.append({vm_info['name']: analyzers_info})


                disk_write_threshold = config.ALERT_THRESHOLDS.get('disk_write_bytes_rate', 0)
                if disk_write_threshold > 0:
                    for dev, rates in io_rate.items():
                        if rates['write_bytes_rate'] > disk_write_threshold:
                            logging.warning(
                                'ALERT: VM %s disk %s write rate %.2f B/s '
                                'exceeds threshold %.2f B/s',
                                vm_info['name'], dev,
                                rates['write_bytes_rate'], disk_write_threshold)

        elif label == 'vcpus_info':

            for i in range(len(vm_stats_info) - 1):
                assert vm_stats_info[i]['uuid'] == vm_stats_info[i+1]['uuid']

                delta_timestamp = (vm_stats_info[i+1]['timestamp']
                                   - vm_stats_info[i]['timestamp'])

                # Calculate per-vCPU utilization from consecutive total_time samples.
                # total_time is in seconds (converted in collector.py).
                # util_pct = Δtotal_time / Δwall_time × 100
                vcpu_utilization = []
                prev_vcpus = vm_stats_info[i]['vcpuinfo']
                curr_vcpus = vm_stats_info[i+1]['vcpuinfo']
                if (delta_timestamp > 0
                        and isinstance(prev_vcpus, list)
                        and isinstance(curr_vcpus, list)
                        and len(prev_vcpus) == len(curr_vcpus)):
                    for prev_v, curr_v in zip(prev_vcpus, curr_vcpus):
                        delta_cpu_time = curr_v['total_time'] - prev_v['total_time']
                        util_pct = round(delta_cpu_time / delta_timestamp * 100, 2)
                        vcpu_utilization.append({
                            'vCPU_num': curr_v['vCPU num'],
                            'state': curr_v['state'],
                            'cpu_util_pct': util_pct,
                            'cpuset': curr_v['cpuset'],
                        })
                analyzers_info = {
                    'vcpu_utilization': vcpu_utilization,
                    'TimeStamp': vm_stats_info[i + 1]['timestamp']
                }
                analyzers_list.append({vm_info['name']: analyzers_info})

        elif label in ['processInfo', 'log_vm']:
            key_map = {
                'processInfo': ['cpu_top5', 'mem_top5'],
                'log_vm': ['current_state', 'latest_event', 'state_log']
            }
            for i in range(len(vm_stats_info) - 1):
                assert vm_stats_info[i]['uuid'] == vm_stats_info[i+1]['uuid']
                analyzers_info = {key: vm_stats_info[i][key] for key in key_map[label]}
                analyzers_info['TimeStamp'] = vm_stats_info[i + 1]['timestamp']
                analyzers_list.append({vm_info['name']: analyzers_info})

        else:
            logging.error('wrong label!')

        return analyzers_list


def print_alerts(alerts):
    """Print alerts to console"""
    if not alerts:
        return
    
    print("\n⚠️  告警信息:")
    print("=" * 60)
    for alert in alerts:
        level = "🔴 严重" if alert["level"] == "critical" else "🟡 警告"
        print(f"{level}: {alert['vm_name']} - {alert['metric']}: {alert['value']}% (阈值: {alert['threshold']}%)")
