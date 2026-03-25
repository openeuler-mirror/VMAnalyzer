# VMAnalyzer API Documentation

## Overview
VMAnalyzer provides a comprehensive API for virtualization monitoring.

## Core Components

### VMCollector
Collects VM statistics from libvirt.

### VMStatsAnalyzer
Analyzes collected statistics.

### VMReporter
Generates reports from analyzed data.

## Usage Example
```python
from agent.collector import VMStatsCollector
collector = VMStatsCollector(vm_factory, storage)
```
