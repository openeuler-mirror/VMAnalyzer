#!/bin/sh
#****************************************************************#
# ScriptName: qemuconsume.sh
# Author: DingLimin
# Function:
#***************************************************************#
CURDATE=$(date "+%Y-%m-%d-%H-%M-%S")
time=20
pid="0"

#dir
qemuconsume_dir=/var/log/vmanalyzer/
perf_svg=${qemuconsume_dir}global_cpuflamegraph-${CURDATE}.svg
datafile=${qemuconsume_dir}qemuconsume-${CURDATE}.log
perf_data=${qemuconsume_dir}perf.${CURDATE}.dat
script_out=${qemuconsume_dir}perf-${CURDATE}.out
folded_out=${qemuconsume_dir}out-${CURDATE}.folded

TOOLS_BIN=/usr/bin/vm_analyer/diagnose/qemuconsume
stackcollapse_file=${TOOLS_BIN}/stackcollapse-perf.pl
flamegraph_file=${TOOLS_BIN}/flamegraph.pl

usage() {
    echo "qemuconsume: show qemu-kvm process consumption"
    echo "options: -h,          help information"
    echo "         -t, time, perf record time, default to 20 seconds"
    echo "         -d <string>, domain name"
}

mk_log_dir() {
    if [ ! -d "$qemuconsume_dir" ];then
        sudo mkdir -p $qemuconsume_dir
    fi
    return 0
}

while getopts 'h' OPT; do
    case $OPT in
        "h")
            usage
            exit 0
            ;;
        "t")
          time="$OPTARG"
          ;;
        "d")
          domain="$OPTARG"
          ;;
        *)
            usage
            exit -1
            ;;
    esac
done

mk_log_dir
