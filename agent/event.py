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
    """Documentation for this component."""
    def __init__(self, uri):
        self.__uri = uri

    @abc.abstractmethod
    def start(self):
        pass

    def get_uri(self):
        return self.__uri

class VMEventLoopNative(VMEventLoop):
    """Documentation for this component."""
    @staticmethod
    def run_loop():
        while True:
            libvirt.virEventRunDefaultImpl()

    def start(self):
        libvirt.virEventRegisterDefaultImpl()
        thread = threading.Thread(target=self.run_loop, name="libvirtEventLoop")
        thread.daemon = True
        thread.start()

    def dom_event_callback(self, conn, dom, event, detail, opaque):
        event_name = (const.VM_DOMAIN_SUPPORTED_EVENTS[event]
                      if 0 <= event < len(const.VM_DOMAIN_SUPPORTED_EVENTS)
                      else str(event))
        logging.debug("dom_event_callback: Domain %s(%s) %s, UUID %s",
                      dom.name(), dom.ID(), event_name, dom.UUIDString())
        vm_id = dom.ID()
        vm_info = {
            "uuid": dom.UUIDString(),
            "name": dom.name(),
            "cpu_util": 0,
        }
        vm_factory = vm.VMFactory()
        if event in (const.VM_DOMAIN_EVENT_CRASHED,
                     const.VM_DOMAIN_EVENT_UNDEFINED,
                     const.VM_DOMAIN_EVENT_STOPPED):
            if vm_id in vm_factory.vms:
                vm_factory.del_vm(vm_id)
        elif event in (const.VM_DOMAIN_EVENT_STARTED,
                       const.VM_DOMAIN_EVENT_DEFINED):
            if vm_id not in vm_factory.vms and vm_id != -1:
                vm_factory.add_vm(vm_id, vm_info)

    def conn_close_callback(self, conn, reason, opaque):
        logging.debug("conn_close_callback: %s: %s",
                      conn.getURI(),
                      const.CONNECTION_CLOSE_REASON_STRINGS.get(reason, str(reason)))
        global run
        run = False
        logging.debug("connection closed, run=%s", run)

def handle_vm_lifecycle_event(event_type, vm_name):
    """Handle VM lifecycle events and trigger alerts"""
    event_messages = {
        "start": f"🟢 VM启动: {vm_name}",
        "stop": f"🔴 VM停止: {vm_name}",
        "pause": f"🟡 VMpaused: {vm_name}",
        "resume": f"🟢 VM恢复: {vm_name}",
        "destroy": f"🔴 VM销毁: {vm_name}",
        "create": f"🆕 VM创建: {vm_name}"
    }
    
    if event_type in event_messages:
        print(f"[事件告警] {event_messages[event_type]}")
