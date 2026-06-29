#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Data integrity test suite for VMAnalyzer."""
import unittest, sys, os, json, tempfile
sys.path.insert(0,os.path.join(os.path.dirname(__file__),".."))

class TestDataIntegrity(unittest.TestCase):
    """Validate data handling, storage, and corruption prevention."""

    def test_session_persistence_roundtrip(self):
        from agent.session_persistence import SessionPersistence
        import time
        with tempfile.NamedTemporaryFile(suffix=".json",delete=False) as f:
            path=f.name
        sp=SessionPersistence(state_file=path)
        sp.set("test_key","test_value")
        sp.set("counter",42)
        sp2=SessionPersistence(state_file=path)
        sp2.restore()
        self.assertEqual(sp2.get("test_key"),"test_value")
        self.assertEqual(sp2.get("counter"),42)
        import os; os.unlink(path)

    def test_compressed_storage(self):
        from agent.compressed_storage import CompressedStorage
        import redis
        try:
            r=redis.Redis(host="localhost",port=6379,socket_connect_timeout=2)
            r.ping()
        except: self.skipTest("Redis not available")
        cs=CompressedStorage(r)
        test_data={"vm":"test1","metrics":{"cpu":45.2,"mem":1024,"ts":1234567890}}
        cs.set("vmanalyzer:test:integrity",test_data)
        result=cs.get("vmanalyzer:test:integrity")
        self.assertEqual(result,test_data)
        r.delete("vmanalyzer:test:integrity")

    def test_anomaly_detector_basic(self):
        from utils.anomaly_detector import AnomalyDetector
        ad=AnomalyDetector(window_size=10,threshold=3.0)
        for i in range(20): ad.add(50.0)
        self.assertFalse(ad.is_anomaly(51.0))
        self.assertTrue(ad.is_anomaly(200.0))

    def test_correlation_analyzer(self):
        from utils.correlation_analyzer import CorrelationAnalyzer
        xs=[1,2,3,4,5,6,7,8,9,10]
        ys=[2,4,6,8,10,12,14,16,18,20]
        r=CorrelationAnalyzer.pearson(xs,ys)
        self.assertIsNotNone(r)
        self.assertAlmostEqual(r["coefficient"],1.0,delta=0.001)

    def test_baseline_manager(self):
        from utils.baseline_manager import BaselineManager
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".json",delete=False) as f:
            path=f.name
        bm=BaselineManager(path=path)
        bm.create_baseline("cpu_baseline",[45,47,44,48,46,45,47])
        result=bm.compare("cpu_baseline",90)
        self.assertIsNotNone(result)
        self.assertTrue(result["pct_change"]>50)
        import os; os.unlink(path)

    def test_quota_manager(self):
        from utils.quota_manager import QuotaManager
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".json",delete=False) as f:
            path=f.name
        qm=QuotaManager(quota_file=path)
        qm.set_quota("test-vm",cpu_pct=80,mem_mb=4096)
        result=qm.check_quota("test-vm",85,3000)
        self.assertTrue(result["exceeded"])
        self.assertIn("cpu",result["violations"])
        result2=qm.check_quota("test-vm",50,2000)
        self.assertFalse(result2["exceeded"])
        import os; os.unlink(path)

if __name__=="__main__":
    unittest.main()

