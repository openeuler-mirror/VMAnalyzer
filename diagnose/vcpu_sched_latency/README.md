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
