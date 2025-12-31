#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
基于esp8266与H618的多功能会议室管理终端
Main Application Entry Point
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from ui.main_window import MainWindow
from config import config


def main():
    # 设置环境变量（如果未设置）
    if 'APP_ENV' not in os.environ:
        # 默认为开发环境，可通过命令行参数或环境变量切换
        if len(sys.argv) > 1 and sys.argv[1] == '--prod':
            os.environ['APP_ENV'] = 'production'
        else:
            os.environ['APP_ENV'] = 'development'

    # 更新配置
    config.environment = os.environ['APP_ENV']
    config.gpio_enabled = config.is_production()

    print(f"运行环境: {config.environment}")
    print(f"GPIO启用: {config.gpio_enabled}")

    if config.is_production():
        print(f"UART端口: {config.uart_port}")
        print(f"UART波特率: {config.uart_baudrate}")

    app = QApplication(sys.argv)
    app.setApplicationName("基于esp8266与H618的多功能会议室管理终端")
    app.setApplicationVersion("1.0.0")

    # 创建主窗口
    window = MainWindow()
    window.setWindowFlags(window.windowFlags() | Qt.WindowType.FramelessWindowHint)
    window.showMaximized()

    exit_code = app.exec()

    sys.exit(exit_code)


if __name__ == "__main__":
    main()