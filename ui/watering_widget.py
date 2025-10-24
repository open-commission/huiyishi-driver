#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
浇水控制界面
用于控制浇水设备并记录操作历史
"""

import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QFrame, QApplication, QPushButton, QListWidget,
                             QListWidgetItem)
from PyQt6.QtCore import Qt, QDateTime, QTimer
from PyQt6.QtGui import QFont, QColor


class WateringWidget(QWidget):
    """
    浇水控制界面
    """
    def __init__(self):
        super().__init__()
        self.watering_status = False  # False表示关闭，True表示开启
        self.operation_history = []  # 操作历史记录
        self.init_ui()
        self.load_sample_history()
        
    def init_ui(self):
        """
        初始化界面
        """
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # 标题
        title_label = QLabel("浇水控制")
        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 状态显示区域
        status_group = QFrame()
        status_group.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        status_layout = QVBoxLayout(status_group)
        
        status_title = QLabel("浇水状态")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        status_title.setFont(font)
        status_layout.addWidget(status_title)
        
        self.status_label = QLabel("浇水设备: 已关闭")
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.status_label.setFont(font)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.update_status_label()
        status_layout.addWidget(self.status_label)
        
        layout.addWidget(status_group)
        
        # 控制按钮区域
        control_group = QFrame()
        control_group.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        control_layout = QVBoxLayout(control_group)
        
        control_title = QLabel("设备控制")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        control_title.setFont(font)
        control_layout.addWidget(control_title)
        
        # 控制按钮
        self.control_button = QPushButton("开启浇水")
        self.control_button.setFixedHeight(60)
        font = QFont()
        font.setPointSize(16)
        self.control_button.setFont(font)
        self.control_button.clicked.connect(self.toggle_watering)
        control_layout.addWidget(self.control_button)
        
        layout.addWidget(control_group)
        
        # 操作历史区域
        history_group = QFrame()
        history_group.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        history_layout = QVBoxLayout(history_group)
        
        history_title = QLabel("操作历史")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        history_title.setFont(font)
        history_layout.addWidget(history_title)
        
        self.history_list = QListWidget()
        history_layout.addWidget(self.history_list)
        
        layout.addWidget(history_group)
        
        # 添加伸缩因子以填满窗口
        layout.addStretch(1)
        
        # 创建定时器用于按钮文本恢复
        self.button_timer = QTimer()
        self.button_timer.setSingleShot(True)
        self.button_timer.timeout.connect(self.reset_button_text)
        
    def toggle_watering(self):
        """
        切换浇水设备状态
        """
        self.watering_status = not self.watering_status
        self.update_status_label()
        
        # 更新按钮文本
        if self.watering_status:
            self.control_button.setText("关闭浇水")
        else:
            self.control_button.setText("开启浇水")
            
        # 记录操作历史
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        status_text = "开启" if self.watering_status else "关闭"
        operation = f"[{timestamp}] 浇水设备{status_text}"
        self.operation_history.append(operation)
        
        # 限制历史记录数量
        if len(self.operation_history) > 50:
            self.operation_history.pop(0)
            
        # 更新历史记录显示
        self.update_history_display()
        
    def update_status_label(self):
        """
        更新状态标签显示
        """
        if self.watering_status:
            self.status_label.setText("浇水设备: 运行中")
            self.status_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.status_label.setText("浇水设备: 已关闭")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
            
    def update_history_display(self):
        """
        更新操作历史显示
        """
        self.history_list.clear()
        # 按时间倒序显示
        for operation in reversed(self.operation_history):
            item = QListWidgetItem(operation)
            if "开启" in operation:
                item.setForeground(QColor("green"))
            else:
                item.setForeground(QColor("red"))
            self.history_list.addItem(item)
            
    def reset_button_text(self):
        """
        恢复按钮文本
        """
        if self.watering_status:
            self.control_button.setText("关闭浇水")
        else:
            self.control_button.setText("开启浇水")
            
    def load_sample_history(self):
        """
        加载示例操作历史
        """
        # 添加一些示例历史记录
        now = QDateTime.currentDateTime()
        self.operation_history = [
            f"[{now.addDays(-1).toString('yyyy-MM-dd hh:mm:ss')}] 浇水设备开启",
            f"[{now.addDays(-1).addSecs(1800).toString('yyyy-MM-dd hh:mm:ss')}] 浇水设备关闭",
            f"[{now.addDays(-1).addSecs(3600*6).toString('yyyy-MM-dd hh:mm:ss')}] 浇水设备开启",
            f"[{now.addDays(-1).addSecs(3600*6 + 1800).toString('yyyy-MM-dd hh:mm:ss')}] 浇水设备关闭"
        ]
        
        self.update_history_display()


if __name__ == "__main__":
    # 测试代码
    app = QApplication(sys.argv)
    widget = WateringWidget()
    widget.show()
    sys.exit(app.exec())