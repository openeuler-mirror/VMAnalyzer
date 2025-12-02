#!/usr/bin/env python
# _*_coding: utf-8 _*_

# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
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
    def __init__(self, vmFactory, statsStorage, label):
        self.__vmFactory = vmFactory
        self.__statsStorage = statsStorage
        self.__label = label


    def recordStats(self):
        vm_factory = self.__vmFactory
        label = self.__label

        if vm_factory is None:
            return

        vc = vm_factory.vc
        stats_info = {}
        for id, vm in list(vm_factory.vms.items()):
            try:
                dom = vc.lookupByUUIDString(vm['uuid'])
            except Exception as err:
                logging.debug('Unable to find VM: %s %s' % (vm['name'], err.message))
                continue
            timestamp = time.time()
            dom_info = dom.info()

            if label == "cpuUsage":

                stats_info[id] = {
                    'uuid': vm['uuid'],
                    'name': vm['name'],
                    'vcpus': dom_info[3],
                    'cputime': dom_info[4],
                    'timestamp': int(timestamp)
                }
                logging.debug("recordStats: Name %s, UUID %s, vcpus %d, cputime %d, timestamp: %d"
                          % (vm['name'], vm['uuid'], dom_info[3], dom_info[4], timestamp))

            elif label == "memoryUsage":

                totalMemory = int(dom_info[1])/1024
                usedMemory = int(dom_info[2])/1024

                stats_info[id] = {
                    'uuid': vm['uuid'],
                    'name': vm['name'],
                    'totalMemory': totalMemory,
                    'usedMemory': usedMemory,
                    'timestamp': int(timestamp)
               }

            elif label == "networkTraffic":

                dom_ifaddr = dom.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_LEASE)

                if not dom_ifaddr:

                    logging.error("Get InterfaceAddresses Filed")
                    stats_info[id] = {
                        'uuid': vm['uuid'],
                        'name': vm['name'],
                        'interfaceAddresses':"null",
                        'networkTraffic':"null",
                        'timestamp': int(timestamp)
                    }

                else:

                    if_addr_dic = {}
                    if_traffic_dic = {}

                    for k,v in dom_ifaddr.items():

                        if_addr_dic[k] = v["hwaddr"]

                        traffic_data_raw = dom.interfaceStats(v["hwaddr"])

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

                    stats_info[id] = {
                        'uuid': vm['uuid'],
                        'name': vm['name'],
                        'interfaceAddresses':if_addr_dic,
                        'networkTraffic':if_traffic_dic,
                        'timestamp': int(timestamp)
                    }
            elif label == "blkio":

                xmldesc = dom.XMLDesc(0)
                doc = libxml2.parseDoc(xmldesc)
                context = doc.xpathNewContext()

                devices =context.xpathEval("/domain/devices/*")

                status_dic = {}
                io_dic = {}

                for device in devices:

                    context.setContextNode(device)
                    res = context.xpathEval("@type")

                    if res is None or len(res) == 0:
                        type = ""
                    else:
                        type = res[0].content

                    if type == "file" or type == "block":

                        res = context.xpathEval("target/@dev")

                        if res is None or len(res) == 0:
                            target_dev = ""
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

                stats_info[id] = {
                    'uuid': vm['uuid'],
                    'name': vm['name'],
                    'blkStatus':status_dic,
                    'blkI/O':io_dic,
                    'timestamp': int(timestamp)
                }


            elif label == "log_vm":

                log_file_path = f"/var/log/libvirt/qemu/{vm['name']}.log"

                if not os.path.exists(log_file_path):
                    logging.error(f"Log file not found: {log_file_path}")
                    continue

                with open(log_file_path, 'r') as log_file:
                    log_content = log_file.readlines()

                current_status = dom.state()[0]
                latest_event = None
                latest_status = None
                status_log = None
                latest_status_line = None
                latest_status_line_number = None
                power_events = ["BOOT", "stop", "shutdown", "destroyed", "error", "SHUTDOWN", "REBOOT", "RESUME"]
                labels_def = {
                        "shutdown": "shutdown",
                        "resume": "running",
                        "error": "false",
                        "stop": "paused",
                        "destroy": "destroy"
                    }

                for line_number in range(len(log_content) - 1, -1, -1):
                    line = log_content[line_number]
                    if "event" in line and latest_event is None:
                        event_start = line.find('"event":') + len('"event":') + 2
                        event_end = line.find('"', event_start)
                        latest_event = line[event_start:event_end].strip()

                    if latest_status is None:
                        if "shutdown" in line or "SHUTDOWN" in line:
                            latest_status = labels_def['shutdown']
                            latest_status_line = line.strip()
                            latest_status_line_number = line_number + 1
                        elif "RESUME" in line:
                            latest_status = labels_def['resume']
                            latest_status_line = line.strip()
                            latest_status_line_number = line_number + 1
                        elif "error" in line:
                            latest_status = labels_def['error']
                            latest_status_line = line.strip()
                            latest_status_line_number = line_number + 1
                        elif "stop" in line:
                            latest_status = labels_def['stop']
                            latest_status_line = line.strip()
                            latest_status_line_number = line_number + 1
                        elif "destroy" in line:
                            latest_status = labels_def['destroy']
                            latest_status_line = line.strip()
                            latest_status_line_number = line_number + 1
                        elif any(event in line for event in power_events):
                            latest_status = "status=other"
                            latest_status_line = line.strip()
                            latest_status_line_number = line_number + 1

                    # Stop looking if we have both event and status
                    if latest_status and latest_status_line_number is not None:
                       latest_status_log = f"log_state:{latest_status} line:{latest_status_line_number} state_line:{latest_status_line}"


                    if latest_event and latest_status:
                        break

                stats_info[id] = {
                    'uuid': vm['uuid'],
                    'name': vm['name'],
                    'current_state': current_status,
                    'latest_event': latest_event,
                    'state_log': latest_status_log,
                    'timestamp': int(timestamp)
                }

            else:
                logging.error("wrong label")

        self.__statsStorage.saveStatsInfo(stats_info)
