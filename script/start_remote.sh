#!/bin/bash

# ==============================
# 配置信息
# ==============================
REMOTE_USER="kickpi"
REMOTE_HOST="192.168.1.128"
REMOTE_PASS="kickpi"
REMOTE_DIR="/home/kickpi/desktop"
REMOTE_PROJECT_DIR="$REMOTE_DIR/huiyishi"

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
# SSH连接参数
# ==============================
SSH_OPTS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
if [ $DEBUG -eq 1 ]; then
    SSH_OPTS="$SSH_OPTS -v"
fi

# ==============================
# 在远程主机上运行应用程序
# ==============================
echo "🚀 正在远程主机上运行应用程序..."

sshpass -p "$REMOTE_PASS" ssh -t $SSH_OPTS "$REMOTE_USER@$REMOTE_HOST" "cd $REMOTE_PROJECT_DIR && source .venv/bin/activate && python main.py"

if [ $? -eq 0 ]; then
    echo "✅ 应用程序运行完成"
else
    echo "❌ 运行应用程序时出错"
    exit 1
fi