
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
