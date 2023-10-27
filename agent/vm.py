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
import libvirt
from utils import wrapper

class VM:
    def __init__(self, uuid):
        self.__uuid = uuid
        self.__name = ""

    @property
    def uuid(self):
        return self.__uuid

    @property
    def name(self):
        return self.__name


@wrapper.singleton
class VMFactory:
    def __init__(self, uri="qemu:///system"):
        self.__vms = {}
        self.__uri = uri
        self.__vc = None

    @property
    def vms(self):
        return self.__vms

    @property
    def vc(self):
        if not self.__vc or self.__vc.isAlive():
            self.__vc = libvirt.openReadOnly(self.__uri)
        return self.__vc

    def addVM(self, vmID, vmInfo):
        vm = self.__vms.get(vmID)
        if vm is not None:
            logging.warning("Already exists VM: %d" % vmID)
            return

        self.__vms[vmID] = vmInfo

    def delVM(self, vmID):
        vm = self.__vms.get(vmID)
        if vm is None:
            logging.warning("No such VM: %d" % vmID)
            return
        del self.__vms[vmID]

def scanActiveVMs():
    vm_factory = VMFactory()
    for dom in vm_factory.vc.listAllDomains():
        if dom.ID() == -1:
            continue
        logging.debug("Domain %s(%s), UUID %s" % (dom.name(), dom.ID(), dom.UUIDString()))
        vm_id = dom.ID()
        # FIXME, We need get analyzers info by libvirt api
        vm_info = {
            'uuid': dom.UUIDString(),
            'name': dom.name(),
            'cpu_util': 0
        }
        if vm_id not in vm_factory.vms:
            vm_factory.addVM(vm_id, vm_info)
