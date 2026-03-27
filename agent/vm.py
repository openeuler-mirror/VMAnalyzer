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
import libvirt
from utils import wrapper


class VM:
    """
    Represents a virtual machine (VM).

    This class encapsulates basic information about a virtual machine,
    including its unique identifier (UUID) and name.
    """
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
    """
    A singleton class responsible for managing virtual machines (VMs).

    This class provides a centralized way to store, retrieve, 
    and manipulate information about virtual machines. 
    It maintains a dictionary of VMs and a connection to the
    libvirt daemon to interact with the virtualization environment.
    """
    def __init__(self, uri="qemu:///system"):
        self.__vms = {}
        self.__uri = uri
        self.__vc = None

    @property
    def vms(self):
        return self.__vms

    @property
    def vc(self):
        if not self.__vc or not self.__vc.isAlive():
            if self.__vc is not None:
                try:
                    self.__vc.close()
                except Exception:
                    pass
            self.__vc = libvirt.openReadOnly(self.__uri)
        return self.__vc

    def get_vm(self, vm_id):
        vm = self.__vms.get(vm_id)
        if vm is None:
            logging.warning("No such VM: %d", vm_id)
            return {}
        return vm

    def add_vm(self, vm_id, vm_info):
        vm = self.__vms.get(vm_id)
        if vm is not None:
            logging.warning("Already exists VM: %d", vm_id)
            return

        self.__vms[vm_id] = vm_info

    def del_vm(self, vm_id):
        vm = self.__vms.get(vm_id)
        if vm is None:
            logging.warning("No such VM: %d", vm_id)
            return
        del self.__vms[vm_id]

    def set_vm_analyzers(self, vm_id, vm_analyzers):
        vm = self.__vms.get(vm_id)
        if vm is None:
            logging.warning("No such VM: %d", vm_id)
            return
        vm["analyzers"] = vm_analyzers

    def get_vm_analyzers(self, vm_id):
        vm = self.__vms.get(vm_id)
        if vm is None:
            logging.warning("No such VM: %d", vm_id)
            return None
        # "analyzers" is only present after set_vm_analyzers() has been called
        # at least once; use .get() to avoid KeyError on first access.
        if "analyzers" not in vm:
            logging.debug("VM %d has no analyzers data yet", vm_id)
            return None
        return vm.get("analyzers")

def scan_active_vms():
    vm_factory = VMFactory()
    for dom in vm_factory.vc.listAllDomains():
        if dom.ID() == -1:
            continue

        state, _ = dom.state()
        if state != libvirt.VIR_DOMAIN_RUNNING:
            logging.debug("Skipping non-running VM %s (state=%d)", dom.name(), state)
            continue

        logging.debug("Domain %s(%s), UUID %s",
                     dom.name(), dom.ID(), dom.UUIDString())
        vm_id = dom.ID()
        # FIXME, We need get analyzers info by libvirt api
        vm_info = {
            "uuid": dom.UUIDString(),
            "name": dom.name(),
            "cpu_util": 0
        }
        if vm_id not in vm_factory.vms:
            vm_factory.add_vm(vm_id, vm_info)

