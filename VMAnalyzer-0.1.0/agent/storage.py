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
import six
import abc
import redis
import json
from utils import config
from utils import wrapper


@six.add_metaclass(abc.ABCMeta)
class VMStatsStorage(object):
    @abc.abstractmethod
    def saveStatsInfo(self, statsInfo):
        pass

    @abc.abstractmethod
    def getStatsInfo(self, vm, startTimestamp, endTimestamp):
        pass


@wrapper.singleton
class VMStatsRedisStorage(VMStatsStorage):
    def __init__(self, vmFactory, label):
        self.__pool = redis.ConnectionPool(host=config.REDIS_DATABASE_CONFIG['host'],
                                           port=config.REDIS_DATABASE_CONFIG['port'])
        self.__sr = redis.StrictRedis(connection_pool=self.__pool)
        self.__vmFactory = vmFactory
        self.__label = label

    @property
    def sr(self):
        return self.__sr

    def saveStatsInfo(self, statsInfo):
        pipe = self.__sr.pipeline()
        pipe.multi()

        label = self.__label

        if label == "cpuUsage":
            for vmID, vmStats in list(statsInfo.items()):
                try:
                    data_dict = {
                        'id': vmID,
                        'name': vmStats['name'],
                        'vcpus': vmStats['vcpus'],
                        'cputime': vmStats['cputime'],
                        'timestamp': vmStats['timestamp']
                    }
                    pipe.zadd(vmStats['uuid'], {json.dumps(data_dict): vmStats['timestamp']})
                except Exception as err:
                    logging.warning('Unable to save stats of %s: %s', vmStats['name'], err.message)

        elif label == "memoryUsage":
            for vmID, vmStats in list(statsInfo.items()):
                try:
                    data_dict = {
                        'id': vmID,
                        'name': vmStats['name'],
                        'totalMemory': vmStats['totalMemory'],
                        'usedMemory': vmStats['usedMemory'],
                        'timestamp': vmStats['timestamp']
                    }
                    pipe.zadd(vmStats['uuid'], {json.dumps(data_dict): vmStats['timestamp']})
                except Exception as err:
                    logging.warning('Unable to save stats of %s: %s', vmStats['name'], err.message)

        elif label == "networkTraffic":
            for vmID, vmStats in list(statsInfo.items()):
                try:
                    data_dict = {
                        'id': vmID,
                        'name': vmStats['name'],
                        'interfaceAddresses': vmStats['interfaceAddresses'],
                        'networkTraffic': vmStats['networkTraffic'],
                        'timestamp': vmStats['timestamp']
                    }
                    pipe.zadd(vmStats['uuid'], {json.dumps(data_dict): vmStats['timestamp']})
                except Exception as err:
                    logging.warning('Unable to save stats of %s: %s', vmStats['name'], err.message)

        elif label == "blkio":
            for vmID, vmStats in list(statsInfo.items()):
                try:
                    data_dict = {
                        'id': vmID,
                        'name': vmStats['name'],
                        'blkStatus': vmStats['blkStatus'],
                        'blkI/O': vmStats['blkI/O'],
                        'timestamp': vmStats['timestamp']
                    }
                    pipe.zadd(vmStats['uuid'], {json.dumps(data_dict): vmStats['timestamp']})
                except Exception as err:
                    logging.warning('Unable to save stats of %s: %s', vmStats['name'], err.message)

        else:
            logging.error("error label!")
        pipe.execute()

    def getStatsInfo(self, vmID, startTimestamp, endTimestamp):
        # VM has been shutdown or destroyed???
        if vmID not in list(self.__vmFactory.vms.keys()):
            return {}

        vm_info = self.__vmFactory.getVM(vmID)
        label = self.__label

        data_list = []
        try:
            data_list = list(self.__sr.zrangebyscore(vm_info['uuid'],
                                                     startTimestamp,
                                                     endTimestamp,
                                                     withscores=True))
        except Exception as err:
            logging.warning('Unable to get stats of %s: %s', vm_info['name'], err.message)

        vm_stats = []
        for data in data_list:
            data_dict = json.loads(data[0])
            # We won't touch this because the VM has been hard rebooted
            if data_dict['id'] != vmID:
                continue

            if label == "cpuUsage":
                stats_dict = {
                    'uuid': vm_info['uuid'],
                    'name': data_dict['name'],
                    'vcpus': data_dict['vcpus'],
                    'cputime': data_dict['cputime'],
                    'timestamp': int(data_dict['timestamp'])
                }

            elif label == "memoryUsage":
                stats_dict = {
                    'uuid': vm_info['uuid'],
                    'name': data_dict['name'],
                    'totalMemory': data_dict['totalMemory'],
                    'usedMemory': data_dict['usedMemory'],
                    'timestamp': int(data_dict['timestamp'])
                }

            elif label == "networkTraffic":
                stats_dict = {
                    'uuid': vm_info['uuid'],
                    'name': data_dict['name'],
                    'interfaceAddresses': data_dict['interfaceAddresses'],
                    'networkTraffic': data_dict['networkTraffic'],
                    'timestamp': int(data_dict['timestamp'])
                }

            elif label == "blkio":
                stats_dict = {
                    'uuid': vm_info['uuid'],
                    'name': data_dict['name'],
                    'blkStatus': data_dict['blkStatus'],
                    'blkI/O': data_dict['blkI/O'],
                    'timestamp': int(data_dict['timestamp'])
                }

            else:
                logging.error('wrong label!')

            vm_stats.append(stats_dict)
        return vm_stats
