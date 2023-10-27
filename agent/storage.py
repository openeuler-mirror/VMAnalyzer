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
    @abc.abstractmethod
    def saveStatsInfo(self, statsInfo):
        pass

    @abc.abstractmethod
    def getStatsInfo(self, vm, startTimestamp, endTimestamp):
        pass


@wrapper.singleton
class VMStatsRedisStorage(VMStatsStorage):
    def __init__(self, vmFactory):
        self.__pool = redis.ConnectionPool(host=config.REDIS_DATABASE_CONFIG['host'],
                                           port=config.REDIS_DATABASE_CONFIG['port'])
        self.__sr = redis.StrictRedis(connection_pool=self.__pool)
        self.__vmFactory = vmFactory

    @property
    def sr(self):
        return self.__sr

    def saveStatsInfo(self, statsInfo):
        pipe = self.__sr.pipeline()
        pipe.multi()
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
        pipe.execute()

    def getStatsInfo(self, vmID, startTimestamp, endTimestamp):
        # VM has been shutdown or destroyed???
        if vmID not in list(self.__vmFactory.vms.keys()):
            return {}

        vm_info = self.__vmFactory.getVM(vmID)

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

            stats_dict = {
                'uuid': vm_info['uuid'],
                'name': data_dict['name'],
                'vcpus': data_dict['vcpus'],
                'cputime': data_dict['cputime'],
                'timestamp': int(data_dict['timestamp'])
            }
            vm_stats.append(stats_dict)
        return vm_stats

