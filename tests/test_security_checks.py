#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Security compliance test suite for VMAnalyzer."""
import unittest, sys, os
sys.path.insert(0,os.path.join(os.path.dirname(__file__),".."))

class TestSecurityChecks(unittest.TestCase):
    """Validate security-related configurations and utilities."""

    def test_security_policy_module_imports(self):
        from utils.security_policy_check import SecurityPolicyCheck
        self.assertTrue(hasattr(SecurityPolicyCheck,"check_host"))
        self.assertTrue(hasattr(SecurityPolicyCheck,"check_vm"))

    def test_security_policy_checks(self):
        from utils.security_policy_check import SecurityPolicyCheck
        checks=SecurityPolicyCheck.CHECKS
        self.assertIsInstance(checks,dict)
        self.assertGreater(len(checks),0)

    def test_backup_verifier_checksum(self):
        from utils.backup_verifier import BackupVerifier
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False,suffix=".test") as f:
            f.write(b"test data for backup verification"); f.flush()
            result=BackupVerifier.verify_backup(f.name)
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["sha256"]),64)

    def test_collection_filter_patterns(self):
        from agent.collection_filter import CollectionFilter
        cf=CollectionFilter()
        cf.add_whitelist(".*")
        self.assertTrue(cf.should_collect("test-vm-01"))
        cf.add_blacklist("test-.*")
        self.assertFalse(cf.should_collect("test-vm-01"))

    def test_taint_tracker(self):
        from utils.taint_tracker import TaintTracker
        tt=TaintTracker()
        tt.add_taint("host1","memory_pressure","high")
        taints=tt.get_taints("host1")
        self.assertEqual(len(taints),1)
        self.assertEqual(taints[0]["key"],"memory_pressure")
        tt.remove_taint("host1","memory_pressure")
        self.assertEqual(len(tt.get_taints("host1")),0)

    def test_maintenance_window(self):
        from utils.maintenance_window import MaintenanceWindow
        import time
        mw=MaintenanceWindow()
        now=time.time()
        mw.add_window(now-60,now+60,["test-vm"],"test window")
        self.assertTrue(mw.is_active("test-vm",now))
        self.assertFalse(mw.is_active("other-vm",now))

if __name__=="__main__":
    unittest.main()

