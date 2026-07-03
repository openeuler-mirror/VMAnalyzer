#!/usr/bin/python
# _*_coding: utf-8 _*_

import libvirt
import sys


LOCAL_NAME = "qemu:///system"
def createConnection(serverName):
    if not serverName:
        print("閿欒锛歴erverName 涓嶈兘涓虹┖")
        sys.exit(1)

    if not libvirt:
        print("閿欒锛氭湭鎵惧埌libvirt搴?)
        sys.exit(1)

    conn = libvirt.openReadOnly(serverName)
    if conn is None:
        print('Failed to connect to QEMU/KVM')
    else:
        return conn

def closeConnection(conn):
    try:
        if conn:
            conn.close()
    except Exception:
        sys.exit(1)

if __name__ == '__main__':

    conn = createConnection(LOCAL_NAME)
    try:
        ccx = conn.virHostGetCCXDesign()
        print("ccx design:")
        print(ccx)
    except libvirt.libvirtError as e:
        print(f'Failed to get CCX Design: {e}')

    closeConnection(conn)
