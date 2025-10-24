#!/bin/bash

# ==============================
# 配置信息
# ==============================
REMOTE_USER="root"
REMOTE_HOST="192.168.1.151"
REMOTE_PASS="kickpi"

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
# 在远程主机上安装Python 3.12
# ==============================
echo "🔧 正在远程主机上安装Python 3.12..."

# 更新包列表
echo "🔄 更新包列表..."
sshpass -p "$REMOTE_PASS" ssh $SSH_OPTS "$REMOTE_USER@$REMOTE_HOST" "echo '$REMOTE_PASS' | sudo -S apt update"

# 安装必要的依赖
echo "📦 安装依赖..."
sshpass -p "$REMOTE_PASS" ssh $SSH_OPTS "$REMOTE_USER@$REMOTE_HOST" "echo '$REMOTE_PASS' | sudo -S apt install -y software-properties-common build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev"

# 添加deadsnakes PPA以获取Python 3.12
echo "🔗 添加deadsnakes PPA..."
sshpass -p "$REMOTE_PASS" ssh $SSH_OPTS "$REMOTE_USER@$REMOTE_HOST" "echo '$REMOTE_PASS' | sudo -S add-apt-repository -y ppa:deadsnakes/ppa"

# 再次更新包列表
echo "🔄 再次更新包列表..."
sshpass -p "$REMOTE_PASS" ssh $SSH_OPTS "$REMOTE_USER@$REMOTE_HOST" "echo '$REMOTE_PASS' | sudo -S apt update"

# 安装Python 3.12及相关组件
echo "🐍 安装Python 3.12..."
sshpass -p "$REMOTE_PASS" ssh $SSH_OPTS "$REMOTE_USER@$REMOTE_HOST" "echo '$REMOTE_PASS' | sudo -S apt install -y python3.12 python3.12-venv python3.12-dev python3.12-distutils"

# 安装pip for Python 3.12
echo "🔗 安装pip..."
sshpass -p "$REMOTE_PASS" ssh $SSH_OPTS "$REMOTE_USER@$REMOTE_HOST" "curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12"

# 将Python 3.12设置为默认Python版本
echo "⚙️ 设置Python 3.12为默认版本..."
sshpass -p "$REMOTE_PASS" ssh $SSH_OPTS "$REMOTE_USER@$REMOTE_HOST" "echo '$REMOTE_PASS' | sudo -S update-alternatives --install /usr/bin/python python /usr/bin/python3.12 1"

# 将pip3设置为默认pip版本
echo "⚙️ 设置pip3为默认pip版本..."
sshpass -p "$REMOTE_PASS" ssh $SSH_OPTS "$REMOTE_USER@$REMOTE_HOST" "echo '$REMOTE_PASS' | sudo -S update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1"

# 添加pip安装路径到PATH环境变量
echo "⚙️ 配置环境变量..."
sshpass -p "$REMOTE_PASS" ssh $SSH_OPTS "$REMOTE_USER@$REMOTE_HOST" "echo 'export PATH=\$PATH:/home/kickpi/.local/bin' >> ~/.bashrc"

# 重新加载环境变量并验证安装
echo "✅ 验证安装..."
sshpass -p "$REMOTE_PASS" ssh $SSH_OPTS "$REMOTE_USER@$REMOTE_HOST" "export PATH=\$PATH:/home/kickpi/.local/bin && python --version && pip --version"

if [ $? -eq 0 ]; then
    echo "🎉 Python 3.12 和 pip 安装完成，并已设置为默认版本"
else
    echo "❌ 安装过程中出现问题"
    exit 1
fi