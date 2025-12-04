import libvirt
from argparse import ArgumentParser

parser = ArgumentParser(description=__doc__)
parser.add_argument("domain")

args = parser.parse_args()

try:
    conn = libvirt.open(None)
except libvirt.libvirtError:
    print("failed to open")
    exit(1)

try:
    dom = conn.lookupByName(args.domain)
except libvirt.libvirtError:
    print("domain is not running")
    exit(0)

downtime = dom.liveupgrade(1, 2000, -1, None)
print(downtime)
