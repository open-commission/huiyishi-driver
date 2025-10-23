#!/bin/bash

# ==============================
# 配置信息
# ==============================
LOCAL_FILE="/home/nebula/dev/stellaris-c-luckfox/cmake-build-debug-luckfox/stellaris_c_luckfox"
REMOTE_USER="root"
REMOTE_HOST="172.32.0.93"
REMOTE_PASS="luckfox"
REMOTE_DIR="/nebula"
REMOTE_FILE="stellaris_c_luckfox"

# ==============================
# 参数处理
# ==============================
DEBUG=0
if [ "$1" == "-d" ]; then
    DEBUG=1
fi

# ==============================
# 检查 sshpass 是否安装
# ==============================
if ! command -v sshpass &> /dev/null
then
    echo "❌ sshpass 未安装，请先安装：sudo apt-get install sshpass"
    exit 1
fi

# ==============================
# 确保远程目录存在
# ==============================
echo "📂 确认远程目录 $REMOTE_DIR 存在..."
SSH_OPTS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
if [ $DEBUG -eq 1 ]; then
    SSH_OPTS="$SSH_OPTS -v"
fi
sshpass -p "$REMOTE_PASS" ssh $SSH_OPTS "$REMOTE_USER@$REMOTE_HOST" "mkdir -p $REMOTE_DIR"

# ==============================
# 执行复制
# ==============================
echo "📤 正在复制文件到远程: $REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/$REMOTE_FILE"
SCP_OPTS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
if [ $DEBUG -eq 1 ]; then
    SCP_OPTS="$SCP_OPTS -v"
fi
sshpass -p "$REMOTE_PASS" scp $SCP_OPTS "$LOCAL_FILE" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/$REMOTE_FILE"

if [ $? -ne 0 ]; then
    echo "❌ 文件复制失败"
    exit 1
fi

# ==============================
# 设置远程执行权限
# ==============================
echo "🔑 正在配置执行权限..."
sshpass -p "$REMOTE_PASS" ssh $SSH_OPTS "$REMOTE_USER@$REMOTE_HOST" "chmod +x $REMOTE_DIR/$REMOTE_FILE"

if [ $? -eq 0 ]; then
    echo "✅ 文件复制并配置执行权限完成"
else
    echo "❌ 设置权限失败"
fi
