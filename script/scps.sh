#!/bin/bash

# ==============================
# 配置信息
# ==============================
LOCAL_DIR="/home/nebula/dev/python-project/qiuyveli"
REMOTE_USER="root"
REMOTE_HOST="192.168.1.128"
REMOTE_PASS="kickpi"
REMOTE_DIR="/home/kickpi/Desktop"
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
# 确保远程目录存在
# ==============================
echo "📂 确认远程目录 $REMOTE_PROJECT_DIR 存在..."
SSH_OPTS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
if [ $DEBUG -eq 1 ]; then
    SSH_OPTS="$SSH_OPTS -v"
fi
sshpass -p "$REMOTE_PASS" ssh $SSH_OPTS "$REMOTE_USER@$REMOTE_HOST" "mkdir -p $REMOTE_PROJECT_DIR"

# ==============================
# 执行复制（使用rsync）排除本地 .venv
# ==============================
echo "📤 正在同步目录到远程: $REMOTE_USER@$REMOTE_HOST:$REMOTE_PROJECT_DIR"

RSYNC_OPTS="-avz --exclude='.venv'"
if [ $DEBUG -eq 1 ]; then
    RSYNC_OPTS="$RSYNC_OPTS -v"
fi

# 使用pv显示传输进度（可选）
if command -v pv &> /dev/null
then
    echo "📊 检测到 pv 工具，将显示传输进度"
    # 先打包本地目录到stdout排除 .venv，再通过pv传输到远程tmp
    TAR_CMD="tar cz --exclude='.venv' -C $(dirname $LOCAL_DIR) $(basename $LOCAL_DIR)"
    sshpass -p "$REMOTE_PASS" bash -c "$TAR_CMD | pv | ssh $SSH_OPTS $REMOTE_USER@$REMOTE_HOST 'tar xz -C /tmp'"
else
    # 不使用pv，直接rsync同步
    sshpass -p "$REMOTE_PASS" rsync $RSYNC_OPTS -e "ssh $SSH_OPTS" "$LOCAL_DIR/" "$REMOTE_PROJECT_DIR/"
fi

# ==============================
# 如果使用pv解压到/tmp，需要同步到最终目录，同时保留远程 .venv
# ==============================
if command -v pv &> /dev/null
then
    sshpass -p "$REMOTE_PASS" ssh $SSH_OPTS "$REMOTE_USER@$REMOTE_HOST" "
cd $REMOTE_PROJECT_DIR
# 备份远程 .venv
if [ -d \"$REMOTE_PROJECT_DIR/.venv\" ]; then
    mv \"$REMOTE_PROJECT_DIR/.venv\" /tmp/.venv_backup 2>/dev/null || :
fi
# 同步/tmp目录到远程项目目录，排除 .venv
rsync -a --exclude='.venv' /tmp/$(basename $LOCAL_DIR)/ $REMOTE_PROJECT_DIR/
# 恢复远程 .venv
if [ -d /tmp/.venv_backup ]; then
    mv /tmp/.venv_backup \"$REMOTE_PROJECT_DIR/.venv\" 2>/dev/null || :
fi
# 清理临时解压目录
rm -rf /tmp/$(basename $LOCAL_DIR)
"
fi

if [ $? -ne 0 ]; then
    echo "❌ 目录同步失败"
    exit 1
fi

echo "✅ 目录同步完成"
