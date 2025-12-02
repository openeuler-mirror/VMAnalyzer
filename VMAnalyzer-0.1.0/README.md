
### Installation Guide

#### 0. Make sure redis server is running

```
# redis-server &

若redis已启动，但步骤2无法执行，请kill后重启服务
```

#### 1. View Help

```
# vm-analyzer-agent --help

usage: vm-analyzer-agent [-hdi] [uri]
   uri will default to qemu:///system
   --help, -h   Print this help message
   --debug, -d  Print debug output
   --interval=SECS, -i  Configure statistics collection interval
   --timeout=SECS, -t  Quit after SECS seconds running
   --memoryUsage, -m  Print detected memory usage
```

#### 2. execute vm-analyzer-agent procedure

```
# vm-analyzer-agent

默认策略为采集CPU利用率周期为1秒，10秒上报一次，CPU利用率显示如下：

...
{"6717da86-fc51-474d-92fe-a76380c27c62": {"Current_cpu_utilization": "13.00%", "TimeStamp": 1598015380}}
{"6717da86-fc51-474d-92fe-a76380c27c62": {"Current_cpu_utilization": "14.00%", "TimeStamp": 1598015381}}
{"6717da86-fc51-474d-92fe-a76380c27c62": {"Current_cpu_utilization": "15.00%", "TimeStamp": 1598015382}}
{"6717da86-fc51-474d-92fe-a76380c27c62": {"Current_cpu_utilization": "16.00%", "TimeStamp": 1598015383}}
{"6717da86-fc51-474d-92fe-a76380c27c62": {"Current_cpu_utilization": "17.00%", "TimeStamp": 1598015384}}
{"6717da86-fc51-474d-92fe-a76380c27c62": {"Current_cpu_utilization": "18.00%", "TimeStamp": 1598015385}}
{"6717da86-fc51-474d-92fe-a76380c27c62": {"Current_cpu_utilization": "19.00%", "TimeStamp": 1598015386}}
{"6717da86-fc51-474d-92fe-a76380c27c62": {"Current_cpu_utilization": "20.00%", "TimeStamp": 1598015387}}
...

```

#### 3. 或者开启调试debug模式：

```
# vm-analyzer-agent -d
```

#### 4. 开启内存利用率检测策略：

```
前提： 支持ballon

# vm-analyzer-agent -m

{"qh-bc8.4": {"Current_mem_utilization": 100.0, "TimeStamp": 1715050794}}
{"qh-bc8.4": {"Current_mem_utilization": 100.0, "TimeStamp": 1715050795}}
{"qh-bc8.4": {"Current_mem_utilization": 100.0, "TimeStamp": 1715050796}}
{"xz-bc8.4": {"Current_mem_utilization": 47.8928, "TimeStamp": 1715050789}}
{"xz-bc8.4": {"Current_mem_utilization": 47.6398, "TimeStamp": 1715050790}}
{"xz-bc8.4": {"Current_mem_utilization": 47.3871, "TimeStamp": 1715050791}}
{"xz-bc8.4": {"Current_mem_utilization": 47.1347, "TimeStamp": 1715050792}}

```

#### 5. 开启网络流量检测策略：

```

# vm-analyzer-agent -n

{"qh-bc8.4": {"interfaceAddresses": {"vnet1": "52:88:99:34:fa:3a"}, "networkTraffic": {"vnet1": {"rx_bytes": 337411141, "rx_packets": 490359, "rx_errs": 0, "rx_drop": 0, "tx_bytes": 181581140, "tx_packets": 78410, "tx_errs": 0, "tx_drop": 0}}, "TimeStamp": 1715222742}}

{"xz-bc8.4": {"interfaceAddresses": {"vnet9": "52:54:00:78:2f:1c", "vnet10": "52:54:00:9b:00:cf"}, "networkTraffic": {"vnet9": {"rx_bytes": 4818498, "rx_packets": 88505, "rx_errs": 0, "rx_drop": 0, "tx_bytes": 335078, "tx_packets": 2350, "tx_errs": 0, "tx_drop": 0}, "vnet10": {"rx_bytes": 4322460, "rx_packets": 80364, "rx_errs": 0, "rx_drop": 0, "tx_bytes": 440782, "tx_packets": 2431, "tx_errs": 0, "tx_drop": 0}}, "TimeStamp": 1715222735}}

interfaceAddresses: 云主机网卡设备MACaddress信息
networkTraffic： 云主机网卡设备网络流量信息

```

#### 6. 开启磁盘I/O检测策略：

```

# vm-analyzer-agent -b

{"qh-win2019": {"blkStatus": {"vda": {"capacity": 32212254720, "allocation": 19854467072, "physical": 19854458880}}, "blkI/O": {"vda": {"read_bytes": 646335, "read_requests": 13906328064, "write_bytes": 246490, "write_requests": 2919450624, "errors": -1}}, "TimeStamp": 1715658674}}
{"dlm-bc8.4": {"blkStatus": {"sdb": {"capacity": 10737418240, "allocation": 1443700736, "physical": 1443561472}}, "blkI/O": {"sdb": {"read_bytes": 10135, "read_requests": 206083072, "write_bytes": 277321, "write_requests": 1835865088, "errors": -1}}, "TimeStamp": 1715658667}}
{"xz-bc8.4": {"blkStatus": {"sdb": {"capacity": 10737418240, "allocation": 3476307968, "physical": 1564475392}, "sdc": {"capacity": 5368709120, "allocation": 5775360, "physical": 4325376}}, "blkI/O": {"sdb": {"read_bytes": 10206, "read_requests": 259564544, "write_bytes": 49368, "write_requests": 409265152, "errors": -1}, "sdc": {"read_bytes": 234, "read_requests": 6680576, "write_bytes": 0, "write_requests": 0, "errors": -1}}, "TimeStamp": 1715658668}}

blkStatus: 磁盘信息
blkI/O： 磁盘I/O信息

```

#### 7. 开启虚机日志检测策略：

```

# vm-analyzer-agent --log_vm


{"test_2110": {"current_state": 1, "latest_event": "NIC_RX_FILTER_CHANGED", "state_log": "line:18710 status line:2024-12-06T09:16:12.130037Z {\"timestamp\": {\"seconds\": 1733476572, \"microseconds\": 130025}, \"event\": \"RESUME\"}", "TimeStamp": 1733476681}}
{"test_2110": {"current_state": 1, "latest_event": "NIC_RX_FILTER_CHANGED", "state_log": "line:18710 status line:2024-12-06T09:16:12.130037Z {\"timestamp\": {\"seconds\": 1733476572, \"microseconds\": 130025}, \"event\": \"RESUME\"}", "TimeStamp": 1733476682}}
{"test_2110": {"current_state": 1, "latest_event": "NIC_RX_FILTER_CHANGED", "state_log": "line:18710 status line:2024-12-06T09:16:12.130037Z {\"timestamp\": {\"seconds\": 1733476572, \"microseconds\": 130025}, \"event\": \"RESUME\"}", "TimeStamp": 1733476683}}

{"test1_2110": {"current_state": 1, "latest_event": "RESUME", "state_log": "line:7555 status line:2024-12-06T09:17:51.336992Z {\"timestamp\": {\"seconds\": 1733476671, \"microseconds\": 336980}, \"event\": \"RESUME\"}", "TimeStamp": 1733476681}}
{"test1_2110": {"current_state": 1, "latest_event": "RESUME", "state_log": "line:7555 status line:2024-12-06T09:17:51.336992Z {\"timestamp\": {\"seconds\": 1733476671, \"microseconds\": 336980}, \"event\": \"RESUME\"}", "TimeStamp": 1733476682}}
{"test1_2110": {"current_state": 1, "latest_event": "RESUME", "state_log": "line:7555 status line:2024-12-06T09:17:51.336992Z {\"timestamp\": {\"seconds\": 1733476671, \"microseconds\": 336980}, \"event\": \"RESUME\"}", "TimeStamp": 1733476683}}

```