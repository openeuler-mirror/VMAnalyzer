#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
# VMAnalyzer Internal API Reference

## Agent Core

### agent/main.py
Entry point for the VM Analyzer agent daemon.
-  - Parse CLI arguments and start monitoring loop
-  - Print help text

### agent/collector.py
-  - Collect VM statistics
  -  - Gather and store stats for all active VMs
  -  - Send command via QEMU Guest Agent
  -  - Execute shell command in guest

### agent/analyze.py
-  - Analyze collected statistics
  -  - Compute utilization and trends

### agent/reporter.py
-  - Report results
  -  - Fetch, analyze, and output results

### agent/storage.py
-  - Redis-backed storage
  -  - Save statistics to Redis
  -  - Retrieve statistics from Redis
  -  - Remove expired data

## Utils

### utils/anomaly_detector.py
-  - Z-score anomaly detection
  -  - Add data point
  -  - Check if value is anomalous

### utils/baseline_manager.py
-  - Performance baseline storage
  -  - Create new baseline
  -  - Compare current value to baseline

## REST API Endpoints

### rest_api.py
-  - List all VMs
-  - Get VM statistics
-  - Get active alerts
-  - Agent health status

## Configuration Files
-  - Redis and alert threshold configuration
-  - Resource quota definitions
-  - VM collection filters
