#!/bin/bash
set -euo pipefail  # 开启严格模式，报错立即退出

# 配置参数（根据实际情况调整）
VM_NAME="xz-win2022"          # 虚拟机名称
USERNAME="Administrator"       # 目标用户名
LOOP_COUNT=60                  # 循环次数
WAIT_AFTER_PING=2              # ping后等待2秒再改密码
WAIT_AFTER_CHANGE=10           # 改密码后等待10秒进入下一轮
PASSWORD_LENGTH=12             # 随机密码长度（8-16位推荐）
SPECIAL_CHARS='@#$%^&*()_+-='  # 允许的特殊字符（避免Windows不兼容字符）

# 日志输出函数（带时间戳）
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# 生成符合规范的随机密码
generate_random_password() {
    # 定义密码各组成部分（确保满足复杂度）
    local upper=$(tr -dc 'A-Z' < /dev/urandom | head -c 2)  # 2个大写字母
    local lower=$(tr -dc 'a-z' < /dev/urandom | head -c 3)  # 3个小写字母
    local digit=$(tr -dc '0-9' < /dev/urandom | head -c 3)  # 3个数字
    local special=$(tr -dc "${SPECIAL_CHARS}" < /dev/urandom | head -c 2)  # 2个特殊字符
    local remaining_length=$((PASSWORD_LENGTH - 2 - 3 - 3 - 2))  # 剩余长度随机填充
    local remaining=$(tr -dc "A-Za-z0-9${SPECIAL_CHARS}" < /dev/urandom | head -c "${remaining_length}")

    # 拼接并打乱字符顺序（避免固定格式）
    local password=$(echo -n "${upper}${lower}${digit}${special}${remaining}" | shuf | tr -d '\n')

    # 输出最终密码（确保长度正确）
    echo "${password}"
}

log "===== QGA循环随机改密码脚本启动 ====="
log "虚拟机名称: ${VM_NAME}"
log "目标用户: ${USERNAME}"
log "密码长度: ${PASSWORD_LENGTH}位（含大小写、数字、特殊字符）"
log "循环次数: ${LOOP_COUNT}次"
log "=================================="

# 循环执行核心逻辑
for ((i=1; i<=LOOP_COUNT; i++)); do
    log "===== 第 ${i}/${LOOP_COUNT} 轮 ====="

    # 1. 生成随机密码并Base64编码（QGA要求）
    PLAIN_PASSWORD=$(generate_random_password)
    BASE64_PASSWORD=$(echo -n "${PLAIN_PASSWORD}" | base64)
    log "生成随机密码: ${PLAIN_PASSWORD}（Base64: ${BASE64_PASSWORD}）"

    # 2. QGA连通性检测（guest-ping）
    log "执行QGA连通性检测（guest-ping）..."
    ping_result=$(virsh qemu-agent-command "${VM_NAME}" '{"execute":"guest-ping"}' 2>&1)
    echo """virsh qemu-agent-command "${VM_NAME}" '{"execute":"guest-ping"}'"""
    echo "${ping_result}"
    if echo "${ping_result}" | grep -q '"return":{}'; then
        log "✅ QGA连通正常"
    else
        log "❌ QGA连通失败！错误信息: ${ping_result}"
        log "跳过本轮改密码，等待${WAIT_AFTER_CHANGE}秒进入下一轮..."
        sleep "${WAIT_AFTER_CHANGE}"
        continue
    fi

    # 3. 等待2秒后修改密码
    log "等待${WAIT_AFTER_PING}秒后执行密码修改..."
    sleep "${WAIT_AFTER_PING}"

    log "执行密码修改（用户名: ${USERNAME}）..."
    change_cmd=$(cat <<EOF
virsh qemu-agent-command ${VM_NAME} '{
    "execute":"guest-set-user-password",
    "arguments":{
        "username":"${USERNAME}",
        "password":"${BASE64_PASSWORD}",
        "crypted":false
    }
}'
EOF
    )
    echo "${change_cmd}"  # 打印完整改密码命令
    change_result=$(eval "${change_cmd}" 2>&1)  # 执行命令并捕获结果
    echo "${change_result}"
    if echo "${change_result}" | grep -q '"return":{}'; then
        log "✅ 密码修改成功（当前密码: ${PLAIN_PASSWORD}）"
    else
        log "❌ 密码修改失败！错误信息: ${change_result}"
        log "当前失败密码: ${PLAIN_PASSWORD}（Base64: ${BASE64_PASSWORD}）"
    fi

    # 4. 等待10秒后进入下一轮
    log "等待${WAIT_AFTER_CHANGE}秒进入下一轮..."
    log "----------------------------------"
    sleep "${WAIT_AFTER_CHANGE}"
done

log "===== 所有${LOOP_COUNT}轮执行完毕 ====="

