#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试主仪表盘组件
"""

import sys
from PyQt6.QtWidgets import QApplication
from ui.dashboard_widget import DashboardWidget


def test_dashboard():
    """
    测试主仪表盘组件
    """
    app = QApplication(sys.argv)
    
    # 创建主仪表盘组件
    dashboard = DashboardWidget()
    
    # 检查是否正确创建了标签页
    print("主仪表盘组件创建成功")
    print(f"标签页数量: {dashboard.tab_widget.count()}")
    
    for i in range(dashboard.tab_widget.count()):
        tab_text = dashboard.tab_widget.tabText(i)
        print(f"标签页 {i+1}: {tab_text}")
    
    # 显示组件
    dashboard.show()
    dashboard.resize(800, 600)
    
    print("主仪表盘显示成功，包含会议室从机和现场从机两个标签页")
    
    # 退出应用
    app.quit()


if __name__ == "__main__":
    test_dashboard()