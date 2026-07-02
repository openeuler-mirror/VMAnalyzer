#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Verify VM backup integrity."""
import subprocess as sp, os, hashlib, logging
LOG=logging.getLogger(__name__)

class BackupVerifier:
    """Check backup file existence, size, and checksums."""
    @staticmethod
    def verify_backup(path):
        if not os.path.exists(path): return {"valid":False,"reason":"file_not_found"}
        size=os.path.getsize(path)
        if size<1024: return {"valid":False,"reason":"file_too_small","size":size}
        sha=hashlib.sha256()
        with open(path,"rb") as f:
            while True:
                chunk=f.read(8192)
                if not chunk: break
                sha.update(chunk)
        return {"valid":True,"size":size,"sha256":sha.hexdigest(),"path":path}

    @staticmethod
    def verify_snapshot(vm_name,snap_name):
        info=sp.run(f"virsh snapshot-info {vm_name} {snap_name} 2>&1",shell=True,capture_output=True,text=True).stdout
        return {"exists":"not found" not in info.lower(),"vm":vm_name,"snapshot":snap_name}
