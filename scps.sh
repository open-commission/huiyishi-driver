#!/bin/bash

# ==============================
# 配置信息
# ==============================
LOCAL_DIR="/home/nebula/dev/python-project/qiuyveli"
REMOTE_USER="root"
REMOTE_HOST="192.168.1.151"
REMOTE_PASS="kickpi"
REMOTE_DIR="/home/kickpi/Desktop"
REMOTE_PROJECT_DIR="$REMOTE_DIR/qiuyveli"

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
# 执行复制
# ==============================
echo "📤 正在复制目录到远程: $REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR"
SCP_OPTS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -r"
if [ $DEBUG -eq 1 ]; then
    SCP_OPTS="$SCP_OPTS -v"
fi

# 添加 pv 工具检查，用于显示进度
PROGRESS_OPT=""
if command -v pv &> /dev/null
then
    echo "📊 检测到 pv 工具，将显示传输进度"
    PROGRESS_OPT="pv"
else
    echo "⚠️ 未检测到 pv 工具，无法显示传输进度（可选安装：sudo apt-get install pv）"
fi

# 创建临时tar包并传输
echo "📦 正在打包并传输目录..."
TEMP_TAR="qiuyveli_$(date +%s).tar.gz"
TEMP_DIR="/tmp"

# 打包本地目录
cd "$LOCAL_DIR/.." || exit 1
tar czf "$TEMP_DIR/$TEMP_TAR" "$(basename $LOCAL_DIR)" 2>/dev/null

# 传输文件
if [ -n "$PROGRESS_OPT" ]; then
    # 使用pv显示进度
    cat "$TEMP_DIR/$TEMP_TAR" | pv | sshpass -p "$REMOTE_PASS" ssh $SSH_OPTS "$REMOTE_USER@$REMOTE_HOST" "cat > $TEMP_DIR/$TEMP_TAR"
else
    # 不显示进度
    sshpass -p "$REMOTE_PASS" scp $SCP_OPTS "$TEMP_DIR/$TEMP_TAR" "$REMOTE_USER@$REMOTE_HOST:$TEMP_DIR/$TEMP_TAR"
fi

# 清理本地临时文件
rm -f "$TEMP_DIR/$TEMP_TAR"

# 解压远程文件并处理权限问题
echo "🔧 正在解压远程文件..."
sshpass -p "$REMOTE_PASS" ssh $SSH_OPTS "$REMOTE_USER@$REMOTE_HOST" "cd /tmp && tar xzf $TEMP_TAR && rm -f $TEMP_TAR && rm -rf $REMOTE_PROJECT_DIR && mv qiuyveli $REMOTE_DIR/"

if [ $? -ne 0 ]; then
    echo "❌ 目录复制失败"
    exit 1
fi

# ==============================
# 在远程主机重建虚拟环境并安装Python依赖
# ==============================
echo "🐍 正在远程主机上重建虚拟环境..."
# 安装系统级PyQt6（如果可用）
sshpass -p "$REMOTE_PASS" ssh $SSH_OPTS "$REMOTE_USER@$REMOTE_HOST" "echo '$REMOTE_PASS' | sudo -S apt update && echo '$REMOTE_PASS' | sudo -S apt install -y python3-pyqt6 python3-pyqt6.qt6-tools || echo '系统包不可用，继续使用pip安装'"

# 创建虚拟环境并安装依赖
sshpass -p "$REMOTE_PASS" ssh $SSH_OPTS "$REMOTE_USER@$REMOTE_HOST" "cd $REMOTE_PROJECT_DIR && export PATH=\$PATH:/home/kickpi/.local/bin && rm -rf .venv && python -m venv .venv && source .venv/bin/activate && pip install --upgrade pip"

# 尝试多种方式安装PyQt6，从最容易到最难
echo "正在尝试安装PyQt6..."
sshpass -p "$REMOTE_PASS" ssh $SSH_OPTS "$REMOTE_USER@$REMOTE_HOST" "cd $REMOTE_PROJECT_DIR && source .venv/bin/activate && pip install --only-binary=PyQt6 PyQt6 pyqt6-sip || pip install PyQt6 pyqt6-sip || pip install --no-build-isolation PyQt6 pyqt6-sip"

# 安装其他依赖
sshpass -p "$REMOTE_PASS" ssh $SSH_OPTS "$REMOTE_USER@$REMOTE_HOST" "cd $REMOTE_PROJECT_DIR && source .venv/bin/activate && pip install numpy>=1.20.0 pyserial>=3.5"

# 安装Qt平台插件依赖，解决PyQt6运行时问题
echo "🎨 安装Qt平台插件依赖..."
sshpass -p "$REMOTE_PASS" ssh $SSH_OPTS "$REMOTE_USER@$REMOTE_HOST" "echo '$REMOTE_PASS' | sudo -S apt install -y libxcb-cursor0 libxcb-cursor-dev qt6-qpa-plugins qt6-base-dev || echo '部分Qt依赖安装失败，但这不会影响基本功能'"
if [ $? -eq 0 ]; then
    echo "✅ 目录复制完成，虚拟环境重建并安装Python依赖成功"
else
    echo "❌ 虚拟环境重建或Python依赖安装失败"
    exit 1
fi