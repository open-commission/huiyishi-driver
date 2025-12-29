#!/bin/bash
set -e

# ===============================
# 配置
# ===============================
PROJECT_DIR="$HOME/Desktop/huiyishi"
VENV_DIR="$PROJECT_DIR/.venv"
PIP_INDEX="https://pypi.mirrors.ustc.edu.cn/simple"

# ===============================
# 更新系统并安装依赖
# ===============================
echo "🔄 更新 apt 包列表..."
sudo apt update

echo "📦 安装系统依赖..."
sudo apt install -y python3 python3-venv python3-pip build-essential \
    libxcb-cursor0 libxcb-cursor-dev qt6-qpa-plugins qt6-base-dev

# ===============================
# 创建项目目录和虚拟环境
# ===============================
echo "🐍 创建项目目录和虚拟环境..."
mkdir -p "$PROJECT_DIR"
python3 -m venv "$VENV_DIR"

# 激活虚拟环境
source "$VENV_DIR/bin/activate"

# 升级 pip 和 setuptools
pip install --upgrade pip setuptools wheel -i $PIP_INDEX

# ===============================
# 安装 PyQt6 及其他 Python 依赖（使用科大镜像）
# ===============================
echo "🔗 安装 PyQt6 及相关依赖..."
pip install --only-binary=:all: "PyQt6" "pyqt6-sip" -i $PIP_INDEX || \
pip install "PyQt6" "pyqt6-sip" -i $PIP_INDEX || \
pip install --no-build-isolation "PyQt6" "pyqt6-sip" -i $PIP_INDEX

# 安装常用 Python 库
pip install "numpy>=1.20.0" "pyserial>=3.5" -i $PIP_INDEX

# ===============================
# 完成
# ===============================
echo "✅ PyQt6 虚拟环境安装完成"
echo "虚拟环境路径: $VENV_DIR"
echo "激活虚拟环境: source $VENV_DIR/bin/activate"

