#!/bin/bash
# 环境检查脚本

echo "Checking VMAnalyzer environment..."
echo "================================"

# Check Python version
python3 --version 2>/dev/null || echo "❌ Python3 not found"

# Check libvirt
virsh --version 2>/dev/null || echo "❌ libvirt not installed"

# Check Redis
redis-cli ping 2>/dev/null || echo "❌ Redis not running"

# Check pip
pip3 --version 2>/dev/null || echo "❌ pip3 not found"

echo "================================"
echo "Environment check completed"
