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

import libvirt
import logging
import threading
import abc
import six
from . import vm
from utils import constants as const

run = True


@six.add_metaclass(abc.ABCMeta)
class VMEventLoop(object):
    def __init__(self, uri):
        self.__uri = uri

    @abc.abstractmethod
    def start(self):
        pass


class VMEventLoopNative(VMEventLoop):

    @staticmethod
    def run_loop():
        while True:
            libvirt.virEventRunDefaultImpl()

    def start(self):
        libvirt.virEventRegisterDefaultImpl()
        thread = threading.Thread(target=self.run_loop, name="libvirtEventLoop")
        thread.setDaemon(True)
        thread.start()


def domEventCallback(self, conn, dom, event, detail, opauque):
    logging.debug("domEventCallback: Domain %s(%s) %s, UUID %s" %
                  (dom.name(), dom.ID(),
                   const.VM_DOMAIN_SUPPORTED_EVENTS[event],
                   dom.UUIDString()))
    vm_id = dom.ID()
    # FIXME, We need get analyzers info by libvirt api
    vm_info = {
        'uuid': dom.UUIDString(),
        'name': dom.name(),
        'analyzers': 30
    }
    vm_factory = vm.VMFactory()
    if event == const.VM_DOMAIN_EVENT_CRASHED or \
       event == const.VM_DOMAIN_EVENT_UNDEFINED:
        if vm_id in vm_factory.vms:
            vm_factory.delVM(vm_id)
    elif event == const.VM_DOMAIN_EVENT_DEFINED:
        if vm_id not in vm_factory.vms:
            vm_factory.addVM(vm_id, vm_info)
