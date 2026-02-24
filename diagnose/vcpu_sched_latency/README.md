vcpu_sched_latency.sh 和 vcpu_sched_switch.sh 说明
概述
这两个脚本用于分析和跟踪虚拟机的 vCPU 调度事件，帮助管理员诊断虚拟机性能问题。vcpu_sched_latency.sh 通过 perf stat 采集调度事件并生成报告，而 vcpu_sched_switch.sh 通过 perf trace 跟踪上下文切换事件并分析其分布和原因。
