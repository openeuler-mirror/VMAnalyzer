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

perf_record() {
    command -v perf > /dev/null
    if [ $? -ne 0 ]; then
        echo "perf command not found" >> $datafile
        return -1
    fi
    local cmd="perf record -g -o ${perf_data} -p ${pid} sleep ${time}"
    echo "Command: $cmd" >> $datafile
    eval $cmd >> $datafile
    return $?
}

perf_convert() {
    #install perl
    command -v perl > /dev/null	
    if [ $? -ne 0 ]; then
        yum install -y perl
        command -v perl > /dev/null
        if [ $? -ne 0 ]; then
            echo "can not install perl" >> $datafile
            return -1
        fi
    fi
    # Generating the call stack
    perf script -i ${perf_data} >${script_out} 2>>$datafile
        if [ $? -ne 0 ]; then
            echo "perf script failed" >> $datafile
            return -1
        fi
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
