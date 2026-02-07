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
import logging
import six
import abc
import redis
import json
from utils import config
from utils import wrapper

@six.add_metaclass(abc.ABCMeta)
class VMStatsStorage(object):
    """
    An abstract base class defining the interface for storing and retrieving
    virtual machine statistics information.
    """
    @abc.abstractmethod
    def save_stats_info(self, stats_info):
        pass

    @abc.abstractmethod
    def get_stats_info(self, vm_id, start_timestamp, end_timestamp):
        pass


@wrapper.singleton
class VMStatsRedisStorage(VMStatsStorage):
    """
    A concrete implementation of the VMStatsStorage abstract base class
    that uses Redis as the storage backend.
    """
    def __init__(self, vm_factory, label):
        self.__pool = redis.ConnectionPool(host=config.REDIS_DATABASE_CONFIG['host'],
                                           port=config.REDIS_DATABASE_CONFIG['port'])
        self.__sr = redis.StrictRedis(connection_pool=self.__pool)
        self.__vm_factory = vm_factory
        self.__label = label

    @property
    def sr(self):
        return self.__sr

    def save_stats_info(self, stats_info):
        pipe = self.__sr.pipeline()
        pipe.multi()
        label = self.__label

        if label == 'cpuUsage':
            for vm_id, vm_stats in list(stats_info.items()):
                try:
                    data_dict = {
                        'id': vm_id,
                        'name': vm_stats['name'],
                        'vcpus': vm_stats['vcpus'],
                        'cputime': vm_stats['cputime'],
                        'timestamp': vm_stats['timestamp']
                    }
                    pipe.zadd(vm_stats['uuid'], {json.dumps(data_dict): vm_stats['timestamp']})
                except Exception as err:
                    logging.warning("Unable to save stats of %s: %s", vm_stats['name'], err.args[0])

        elif label == 'memoryUsage':
            for vm_id, vm_stats in list(stats_info.items()):
                try:
                    data_dict = {
                        'id': vm_id,
                        'name': vm_stats['name'],
                        'totalMemory': vm_stats['totalMemory'],
                        'usedMemory': vm_stats['usedMemory'],
                        'timestamp': vm_stats['timestamp']
                    }
                    pipe.zadd(vm_stats['uuid'],
                              {json.dumps(data_dict): vm_stats['timestamp']})
                except Exception as err:
                    logging.warning('Unable to save stats of %s: %s',
                                    vm_stats['name'], err.args)

        elif label == 'networkTraffic':
            for vm_id, vm_stats in list(stats_info.items()):
                try:
                    data_dict = {
                        'id': vm_id,
                        'name': vm_stats['name'],
                        'interfaceAddresses': vm_stats['interfaceAddresses'],
                        'networkTraffic': vm_stats['networkTraffic'],
                        'timestamp': vm_stats['timestamp']
                    }
                    pipe.zadd(vm_stats['uuid'],
                              {json.dumps(data_dict): vm_stats['timestamp']})
                except Exception as err:
                    logging.warning('Unable to save stats of %s: %s',
                                    vm_stats['name'], err.args)

        elif label == 'blkio':
            for vm_id, vm_stats in list(stats_info.items()):
                try:
                    data_dict = {
                        'id': vm_id,
                        'name': vm_stats['name'],
                        'blkStatus': vm_stats['blkStatus'],
                        'blkI/O': vm_stats['blkI/O'],
                        'timestamp': vm_stats['timestamp']
                    }
                    pipe.zadd(vm_stats['uuid'],
                              {json.dumps(data_dict): vm_stats['timestamp']})
                except Exception as err:
                    logging.warning('Unable to save stats of %s: %s',
                                    vm_stats['name'], err.args)

        elif label == 'log_vm':
            for vm_id, vm_stats in list(stats_info.items()):
                try:
                    data_dict = {
                        'id': vm_id,
                        'name': vm_stats['name'],
                        'current_state': vm_stats['current_state'],
                        'latest_event': vm_stats['latest_event'],
                        'state_log': vm_stats['state_log'],
                        'timestamp': vm_stats['timestamp']
                    }
                    pipe.zadd(vm_stats['uuid'],
                              {json.dumps(data_dict): vm_stats['timestamp']})
                except Exception as err:
                    logging.warning('Unable to save stats of %s: %s',
                                    vm_stats['name'], err.args)

        else:
            logging.error('wrong label!')
        pipe.execute()

    def get_stats_info(self, vm_id, start_timestamp, end_timestamp):
        # VM has been shutdown or destroyed???
        if vm_id not in list(self.__vm_factory.vms.keys()):
            return {}

        vm_info = self.__vm_factory.get_vm(vm_id)
        label = self.__label

        data_list = []
        try:
            data_list = list(self.__sr.zrangebyscore(vm_info['uuid'],
                                                     start_timestamp,
                                                     end_timestamp,
                                                     withscores=True))
        except Exception as err:
            logging.warning("Unable to get stats of %s: %s", vm_info['name'], err.args[0])

        vm_stats = []
        for data in data_list:
            data_dict = json.loads(data[0])
            # We won't touch this because the VM has been hard rebooted
            if data_dict['id'] != vm_id:
                continue
            if label == 'cpuUsage':
                stats_dict = {
                    'uuid': vm_info['uuid'],
                    'name': data_dict['name'],
                    'vcpus': data_dict['vcpus'],
                    'cputime': data_dict['cputime'],
                    'timestamp': int(data_dict['timestamp'])
                }

            elif label == 'memoryUsage':
                stats_dict = {
                    'uuid': vm_info['uuid'],
                    'name': data_dict['name'],
                    'totalMemory': data_dict['totalMemory'],
                    'usedMemory': data_dict['usedMemory'],
                    'timestamp': int(data_dict['timestamp'])
                }
            elif label == 'networkTraffic':
                stats_dict = {
                    'uuid': vm_info['uuid'],
                    'name': data_dict['name'],
                    'interfaceAddresses': data_dict['interfaceAddresses'],
                    'networkTraffic': data_dict['networkTraffic'],
                    'timestamp': int(data_dict['timestamp'])
                }

            elif label == 'blkio':
                stats_dict = {
                    'uuid': vm_info['uuid'],
                    'name': data_dict['name'],
                    'blkStatus': data_dict['blkStatus'],
                    'blkI/O': data_dict['blkI/O'],
                    'timestamp': int(data_dict['timestamp'])
                }

            elif label == 'log_vm':
                stats_dict = {
                    'uuid': vm_info['uuid'],
                    'name': data_dict['name'],
                    'current_state': data_dict['current_state'],
                    'latest_event': data_dict['latest_event'],
                    'state_log': data_dict['state_log'],
                    'timestamp': int(data_dict['timestamp'])
                }

            else:
                logging.error('wrong label!')

            vm_stats.append(stats_dict)

        return vm_stats
