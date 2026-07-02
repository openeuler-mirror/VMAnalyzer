#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
# VMAnalyzer Performance Tuning Guide

## CPU Tuning
- **CPU Pinning:** Pin vCPUs to physical cores to reduce context switching
  
- **CPU Model:** Use host-passthrough for best performance
- **vCPU Count:** Do not over-allocate; monitor steal time

## Memory Tuning
- **Huge Pages:** Enable 2MB or 1GB huge pages for large-memory VMs
- **Balloon Driver:** Install virtio-balloon driver in guest for dynamic memory
- **KSM:** Enable KSM to deduplicate memory across VMs (saves 10-40%)

## Disk I/O Tuning
- **Cache Mode:** Use  for data safety or  for performance
- **IO Threads:** Assign dedicated IOThreads per disk
- **Throttling:** Set QoS limits to prevent noisy-neighbor issues
- **Block Size:** Align partitions to 4K boundaries

## Network Tuning
- **Multi-Queue:** Enable multi-queue vNICs (queues = vCPUs)
- **vhost-net:** Ensure vhost-net kernel module is loaded
- **TSO/GSO:** Disable if experiencing packet loss
- **Jumbo Frames:** Consider for high-throughput workloads

## NUMA Tuning
- Pin VM memory to the same NUMA node as its vCPUs
- Use  in VM XML to enforce NUMA policies

## Monitoring Best Practices
- Set appropriate thresholds to avoid alert fatigue
- Use incremental collection for large-scale deployments
- Archive historical data for trend analysis
