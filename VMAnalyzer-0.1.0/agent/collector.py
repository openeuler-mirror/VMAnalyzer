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

            else:
                logging.error("wrong label")

        self.__statsStorage.saveStatsInfo(stats_info)
