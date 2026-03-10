#!/usr/bin/python
# _*_coding: utf-8 _*_

import libvirt
import sys


LOCAL_NAME = "qemu:///system"
def createConnection(serverName):
    if not libvirt:
        sys.exit(1)

    conn = libvirt.openReadOnly(serverName)
    if conn == None:
        print('Failed to connect to QEMU/KVM')
    else:
        return conn

def closeConnection(conn):
    try:
        conn.close()
    except:
        sys.exit(1)

if __name__ == '__main__':

    conn = createConnection(LOCAL_NAME)
    ccx = conn.virHostGetCCXDesign()
    print("ccx design:")
    print(ccx)

    closeConnection(conn)
