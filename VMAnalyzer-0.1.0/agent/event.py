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
    """
    `VMEventLoop` 是一个抽象基类，用于定义虚拟机事件循环的基本接口。

    该类主要负责初始化虚拟机连接的 URI，并提供一个抽象方法 `start`，
    任何继承自 `VMEventLoop` 的具体类都需要实现此方法，以启动相应的虚拟机事件循环。
    """
    def __init__(self, uri):
        self.__uri = uri

    @abc.abstractmethod
    def start(self):
        pass

    def get_uri(self):
        return self.__uri

class VMEventLoopNative(VMEventLoop):
    """
    `VMEventLoopNative` 类继承自 `VMEventLoop`，用于实现基于 `libvirt` 的原生虚拟机事件循环。

    该类提供了一个静态方法 `run_loop` 用于持续运行默认的 `libvirt` 事件循环，
    并实现了 `VMEventLoop` 中的抽象方法 `start`，用于注册默认的 `libvirt` 事件处理函数，
    并在一个守护线程中启动事件循环。
    """
    @staticmethod
    def run_loop():
        while True:
            libvirt.virEventRunDefaultImpl()

    def start(self):
        libvirt.virEventRegisterDefaultImpl()
        thread = threading.Thread(target=self.run_loop, name="libvirtEventLoop")
        thread.setDaemon(True)
        thread.start()


    def dom_event_callback(self, conn, dom, event, detail, opaque):
        logging.debug("dom_event_callback: Domain %s(%s) %s, UUID %s",
                      dom.name(), dom.ID(),
                      const.VM_DOMAIN_SUPPORTED_EVENTS[event],
                      dom.UUIDString())
        vm_id = dom.ID()
        # FIXME, We need get analyzers info by libvirt api
        vm_info = {
                   "uuid": dom.UUIDString(),
                   "name": dom.name(),
                   "analyzers": 30
                  }
        vm_factory = vm.VMFactory()
        if event == const.VM_DOMAIN_EVENT_CRASHED or \
           event == const.VM_DOMAIN_EVENT_UNDEFINED:
            if vm_id in vm_factory.vms:
                vm_factory.del_vm(vm_id)
        elif event == const.VM_DOMAIN_EVENT_DEFINED:
            if vm_id not in vm_factory.vms:
                vm_factory.add_vm(vm_id, vm_info)


    def conn_close_callback(self, conn, reason, opaque):
        logging.debug("conn_close_callback: %s: %s",
                      conn.getURI(),
                      const.CONNECTION_CLOSE_REASON_STRINGS[reason])
        global run
        run = False
        logging.debug("status is %s", run)
