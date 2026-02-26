vcpu_sched_latency.sh 和 vcpu_sched_switch.sh 说明
概述
这两个脚本用于分析和跟踪虚拟机的 vCPU 调度事件，帮助管理员诊断虚拟机性能问题。vcpu_sched_latency.sh 通过 perf stat 采集调度事件并生成报告，而 vcpu_sched_switch.sh 通过 perf trace 跟踪上下文切换事件并分析其分布和原因。

脚本功能
vcpu_sched_latency.sh
功能：

使用 perf stat 采集 vCPU 调度事件（如睡眠、I/O 等待、阻塞、上下文切换等）。

生成调度事件的分析报告，包括事件计数和占比。

检测高延迟原因（如 I/O 等待、资源阻塞、任务迁移等）。

适用场景：

分析虚拟机的整体调度性能。

诊断虚拟机的高延迟问题。

vcpu_sched_switch.sh
功能：

使用 perf trace 跟踪指定 vCPU 线程的上下文切换事件。

分析上下文切换的总数、平均切换时间及切换原因分布。

适用场景：

深入分析某个 vCPU 线程的上下文切换行为。

诊断上下文切换频繁或延迟过高的问题。

使用方法
1. 运行 vcpu_sched_latency.sh
命令格式：
sudo bash vcpu_sched_latency.sh <VM_NAME>
参数：

<VM_NAME>：虚拟机的名称（如 vm1）。

输出：

日志文件：/var/log/vmanalyzer/vcpu_sched_latency-<时间戳>.log。

报告内容：

调度事件的计数和占比。

高延迟警告（如 I/O 等待、资源阻塞等）。

示例：
sudo bash vcpu_sched_latency.sh vm1

2. 运行 vcpu_sched_switch.sh
命令格式：
sudo bash vcpu_sched_switch.sh <VM_NAME> <VCPU_ID>
参数：

<VM_NAME>：虚拟机的名称（如 vm1）。

<VCPU_ID>：vCPU 的编号（如 0 表示第一个 vCPU）。

输出：

日志文件：/var/log/vmanalyzer/vcpu_sched_trace-<时间戳>.log。

报告内容：

上下文切换的总数和平均时间。

切换原因的分布（如 S、R 等）。
