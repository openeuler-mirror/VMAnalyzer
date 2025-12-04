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
import time
import libvirt
import libxml2
import os


class VMStatsCollector:
    """
    A class responsible for collecting and recording various 
    statistics of virtual machines (VMs).

    This class interacts with a VM factory to get information about VMs, 
    and then retrieves different types of statistics (such as CPU usage,
    memory usage, network traffic, block I/O, and log information) for each VM.
    The collected statistics are then saved to a specified storage.
    """
    def __init__(self, vm_factory, stats_storage, label):
        self.__vm_factory = vm_factory
        self.__stats_storage = stats_storage
        self.__label = label


    def record_stats(self):
        vm_factory = self.__vm_factory
        label = self.__label

        if vm_factory is None:
            return

        vc = vm_factory.vc
        stats_info = {}
        for vm_id, vm in list(vm_factory.vms.items()):
            try:
                dom = vc.lookupByUUIDString(vm['uuid'])
            except Exception as err:
                logging.debug('Unable to find VM: %s %s',
                              vm['name'], err.args)
                continue
            timestamp = time.time()

            dom_info = dom.info()

            if label == 'cpuUsage':

                stats_info[vm_id] = {
                    'uuid': vm['uuid'],
                    'name': vm['name'],
                    'vcpus': dom_info[3],
                    'cputime': dom_info[4],
                    'timestamp': int(timestamp)
                }
                logging.debug(
                    'recordStats: Name %s, UUID %s, '
                    'vcpus %d, cputime %d, timestamp: %d',
                    vm['name'], vm['uuid'], dom_info[3],
                    dom_info[4], timestamp)

            elif label == 'memoryUsage':
                memstat = dom.memoryStats()
                total_memory = int(memstat["actual"]) / 1024
                available_memory = int(memstat["available"]) / 1024
                used_memory = total_memory - available_memory

                stats_info[vm_id] = {
                    'uuid': vm['uuid'],
                    'name': vm['name'],
                    'totalMemory': total_memory,
                    'usedMemory': used_memory,
                    'timestamp': int(timestamp)
               }

            elif label == 'networkTraffic':

                dom_ifaddr = dom.interfaceAddresses(
                    libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_LEASE)

                if not dom_ifaddr:

                    logging.error('Get InterfaceAddresses Failed')
                    stats_info[vm_id] = {
                        'uuid': vm['uuid'],
                        'name': vm['name'],
                        'interfaceAddresses':'null',
                        'networkTraffic':'null',
                        'timestamp': int(timestamp)
                    }

                else:

                    if_addr_dic = {}
                    if_traffic_dic = {}

                    for k,v in dom_ifaddr.items():

                        if_addr_dic[k] = v['hwaddr']

                        traffic_data_raw = dom.interfaceStats(v['hwaddr'])

                        traffic_data = {
                                'rx_bytes': traffic_data_raw[0],
                                'rx_packets': traffic_data_raw[1],
                                'rx_errs': traffic_data_raw[2],
                                'rx_drop': traffic_data_raw[3],
                                'tx_bytes': traffic_data_raw[4],
                                'tx_packets': traffic_data_raw[5],
                                'tx_errs': traffic_data_raw[6],
                                'tx_drop': traffic_data_raw[7]
                                }

                        if_traffic_dic[k] = traffic_data

                    stats_info[vm_id] = {
                        'uuid': vm['uuid'],
                        'name': vm['name'],
                        'interfaceAddresses':if_addr_dic,
                        'networkTraffic':if_traffic_dic,
                        'timestamp': int(timestamp)
                    }
            elif label == 'blkio':

                xmldesc = dom.XMLDesc(0)
                doc = libxml2.parseDoc(xmldesc)
                context = doc.xpathNewContext()

                devices =context.xpathEval('/domain/devices/disk')

                status_dic = {}
                io_dic = {}

                for device in devices:

                    context.setContextNode(device)
                    res = context.xpathEval('@type')

                    if res is None or len(res) == 0:
                        dev_type = ''
                    else:
                        dev_type = res[0].content

                    if dev_type == 'file' or dev_type == 'block' or dev_type == 'network':

                        res = context.xpathEval('target/@dev')

                        if res is None or len(res) == 0:
                            target_dev = ''
                        else:
                            target_dev = res[0].content

                            target_dev_status = {}
                            tmp = dom.blockInfo(target_dev)

                            target_dev_status['capacity'] = tmp[0]
                            target_dev_status['allocation'] = tmp[1]
                            target_dev_status['physical'] = tmp[2]

                            status_dic[target_dev] = target_dev_status

                            target_dev_io = {}
                            tmp = dom.blockStats(target_dev)

                            target_dev_io['read_bytes'] = tmp[0]
                            target_dev_io['read_requests'] = tmp[1]
                            target_dev_io['write_bytes'] = tmp[2]
                            target_dev_io['write_requests'] = tmp[3]
                            target_dev_io['errors'] = tmp[4]

                            io_dic[target_dev] = target_dev_io

                stats_info[vm_id] = {
                    'uuid': vm['uuid'],
                    'name': vm['name'],
                    'blkStatus':status_dic,
                    'blkI/O':io_dic,
                    'timestamp': int(timestamp)
                }

            elif label == 'vcpus_info':
                result = dom.vcpus()
                if result is None:
                    logging.error("get vcpus info failed")
                    stats_info[vm_id] = {
                        'uuid': vm['uuid'],
                        'name': vm['name'],
                        'vcpuinfo':'null',
                        'timestamp': int(timestamp)
                    }

                if not result or len(result) != 2:
                    logging.error("unvalid result")
                    stats_info[vm_id] = {
                        'uuid': vm['uuid'],
                        'name': vm['name'],
                        'vcpuinfo':'null',
                        'timestamp': int(timestamp)
                    }

                vcpu_info_list, cpumap_list = result
                parsed_configs = []

                state_map = {
                    0: "离线/睡眠",
                    1: "运行中",
                    2: "暂停",
                    3: "崩溃",
                    4: "未初始化"
                }

                for idx, (vcpu_info, cpumap) in enumerate(zip(vcpu_info_list, cpumap_list)):
                    vcpu_id = vcpu_info[0]
                    state_code = vcpu_info[1]
                    total_time_ns = vcpu_info[2]
                    current_phy_cpu = vcpu_info[3]

                    allowed_phy_cpus = []
                    for cpu_num, is_allowed in enumerate(cpumap):
                        if is_allowed:
                            allowed_phy_cpus.append(cpu_num)

                    total_time_s = round(total_time_ns / 1e9, 2)
                    parsed_configs.append({
                        "index": idx + 1,
                        "vCPU num": vcpu_id,
                        "state": state_map.get(state_code, f"UNKNOWN({state_code})"),
                        "total_time": total_time_s,
                        "cpuset": allowed_phy_cpus,
                        "allow pin CPU count": len(allowed_phy_cpus)
                    })

                stats_info[vm_id] = {
                    'uuid': vm['uuid'],
                    'name': vm['name'],
                    'vcpuinfo':parsed_configs,
                    'timestamp': int(timestamp)
                }
     
            elif label == 'log_vm':

                log_file_path = f"/var/log/libvirt/qemu/{vm['name']}.log"

                if not os.path.exists(log_file_path):
                    logging.error('Log file not found: %s', log_file_path)
                    continue

                with open(log_file_path, 'r', encoding='utf-8') as log_file:
                    log_content = log_file.readlines()

                current_status = dom.state()[0]
                latest_event = None
                latest_status = None
                latest_status_log = None
                latest_status_line = None
                latest_status_line_number = None
                power_events = ['BOOT', 'stop', 'shutdown', 'destroyed',
                                'error', 'SHUTDOWN', 'REBOOT', 'RESUME']
                labels_def = {
                        'shutdown': 'shutdown',
                        'resume': 'running',
                        'error': 'false',
                        'stop': 'paused',
                        'destroy': 'destroy'
                    }

                for line_number in range(len(log_content) - 1, -1, -1):
                    line = log_content[line_number]
                    if 'event' in line and latest_event is None:
                        event_start = \
                            line.find('"event":') + len('"event":') + 2
                        event_end = line.find('"', event_start)
                        latest_event = line[event_start:event_end].strip()

                    if latest_status is None:
                        if 'shutdown' in line or 'SHUTDOWN' in line:
                            latest_status = labels_def['shutdown']
                            latest_status_line = line.strip()
                            latest_status_line_number = line_number + 1
                        elif 'RESUME' in line:
                            latest_status = labels_def['resume']
                            latest_status_line = line.strip()
                            latest_status_line_number = line_number + 1
                        elif 'error' in line:
                            latest_status = labels_def['error']
                            latest_status_line = line.strip()
                            latest_status_line_number = line_number + 1
                        elif 'stop' in line:
                            latest_status = labels_def['stop']
                            latest_status_line = line.strip()
                            latest_status_line_number = line_number + 1
                        elif 'destroy' in line:
                            latest_status = labels_def['destroy']
                            latest_status_line = line.strip()
                            latest_status_line_number = line_number + 1
                        elif any(event in line for event in power_events):
                            latest_status = 'status=other'
                            latest_status_line = line.strip()
                            latest_status_line_number = line_number + 1

                    # Stop looking if we have both event and status
                    if latest_status and latest_status_line_number is not None:
                        latest_status_log = f'log_state:{latest_status} ' \
                                        f'line:{latest_status_line_number} '\
                                        f'state_line:{latest_status_line}'


                    if latest_event and latest_status:
                        break

                stats_info[vm_id] = {
                    'uuid': vm['uuid'],
                    'name': vm['name'],
                    'current_state': current_status,
                    'latest_event': latest_event,
                    'state_log': latest_status_log,
                    'timestamp': int(timestamp)
                }

            else:
                logging.error('wrong label')

        self.__stats_storage.save_stats_info(stats_info)
