#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
# VMAnalyzer Troubleshooting Guide

## Common Issues

### 1. No data showing for VMs
- Check libvirt connection: 
- Verify QEMU Guest Agent is installed and running
- Check Redis connection: 
- Ensure vmanalyzer agent has proper permissions

### 2. High CPU steal time
- Check for CPU overcommit
- Reduce vCPU count or enable CPU pinning
- Verify host CPU governor is set to performance

### 3. Memory balloon not working
- Install virtio-balloon driver in guest OS
- Check  output
- Verify balloon driver is loaded: 

### 4. Network drops
- Check vhost-net kernel module: 
- Verify multi-queue configuration matches vCPU count
- Check switch/bridge MTU settings
- Monitor interrupt affinity

### 5. Disk I/O latency spikes
- Check disk cache mode with 
- Verify IOThread configuration
- Check storage pool health
- Consider SSD or NVMe for latency-sensitive workloads

### 6. Migration failures
- Verify shared storage is accessible on both hosts
- Check CPU compatibility between hosts
- Ensure sufficient memory on target host
- Check for passthrough devices that block migration

### 7. Agent crashes or hangs
- Check logs at 
- Verify Python dependencies are installed
- Check available file descriptors: 1048576
- Restart with  flag for verbose logging

## Diagnostic Commands

