#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
秋月梨种植环境监测与生产溯源管理系统
Main Application Entry Point
"""

import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("秋月梨种植环境监测与生产溯源管理系统")
    app.setApplicationVersion("1.0.0")
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()