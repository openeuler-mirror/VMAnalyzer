#!/usr/bin/python
""" information."""

#
# Get disk serial info from a domain
#

import libvirt
import sys
from lxml import etree
import shlex
import logging
LOG = logging.getLogger(__name__)


SERVER_NAME = "qemu+ssh://root@192.168.203.132/system"
LOCAL_NAME = "qemu:///system"
def createConnection(serverName):
  if not libvirt:
    LOG.debug('python-libvirt module is missing')
    sys.exit(1)
#  conn = libvirt.openReadOnly("qemu+ssh://root@192.168.203.132/system")
  conn = libvirt.openReadOnly(serverName)
  if conn == None:
    LOG.debug('Failed to connect to QEMU/KVM')
  else:
    LOG.debug('------------Connected to QEMU/KVM---------------')
    return conn
  
def closeConnection(conn):
  try:
    LOG.debug('----------Disconnect from QEMU/KVM--------------')
    conn.close()
  except (ValueError, TypeError, KeyError):
    LOG.debug('Failed to close connection')
    sys.exit(1)

def getESSDSerial(domain, conn):
  if domain == None:
    LOG.debug('Domain Name Is Empty')
    sys.exit(1)
  try:
      dom = conn.lookupByName(domain)
  except libvirt.libvirtError as e:
    LOG.debug(f'Failed to lookup domain {domain}: {e}')
    sys.exit(1)

  tree = etree.fromstring(dom.XMLDesc(0))
  for disk_info in tree.findall('devices/disk'):
    device = disk_info.find('target').get('dev')
    if device and (device.startswith('sd') or device.startswith('vd')):
      serial = disk_info.find('serial')
      volume_uuid = serial.text if serial is not None else None
      LOG.debug('disk: %s / serial : %s ' % (device, volume_uuid))

if __name__ == '__main__':
  argc = len(sys.argv) - 1
  LOG.debug(argc)
  if argc == 0:
      libvirtServer = "qemu:///system"
  else:
      libvirtServer = "qemu+ssh://root@" + sys.argv[1] + "/system"
  conn = createConnection(libvirtServer)
  #getESSDSerial(domainName, conn)
  pack = conn.getLibPackage()
  ver = conn.getLibVersion()
  LOG.debug("libvirt version : {}\nlibvert package info : {}".format(ver, pack))

  closeConnection(conn)
  


