#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
设备控制界面
用于控制现场设备并记录操作历史
"""

import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QFrame, QApplication, QPushButton, QListWidget,
                             QListWidgetItem, QSizePolicy, QCheckBox, QGroupBox)
from PyQt6.QtCore import Qt, QDateTime, QTimer
from PyQt6.QtGui import QFont, QColor


class WateringWidget(QWidget):
    """
    设备控制界面
    """
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.motor_status = False  # 电机状态 False表示关闭，True表示开启
        self.light_status = False  # 照明状态
        self.ac_status = False     # 空调状态
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
        title_label = QLabel("设备控制")
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
        
        status_title = QLabel("设备状态")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        status_title.setFont(font)
        status_layout.addWidget(status_title)
        
        # 电机状态
        self.motor_status_label = QLabel("电机状态: 未激活")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.motor_status_label.setFont(font)
        self.motor_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.update_motor_status_label()
        status_layout.addWidget(self.motor_status_label)
        
        # 照明状态
        self.light_status_label = QLabel("照明状态: 未激活")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.light_status_label.setFont(font)
        self.light_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.update_light_status_label()
        status_layout.addWidget(self.light_status_label)
        
        # 空调状态
        self.ac_status_label = QLabel("空调状态: 未激活")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.ac_status_label.setFont(font)
        self.ac_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.update_ac_status_label()
        status_layout.addWidget(self.ac_status_label)
        
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
        
        # 电机控制按钮
        self.motor_control_button = QPushButton("启动电机")
        self.motor_control_button.setFixedHeight(60)
        font = QFont()
        font.setPointSize(16)
        self.motor_control_button.setFont(font)
        self.motor_control_button.clicked.connect(self.toggle_motor)
        control_layout.addWidget(self.motor_control_button)
        
        # 照明控制按钮
        self.light_control_button = QPushButton("开关照明")
        self.light_control_button.setFixedHeight(60)
        font = QFont()
        font.setPointSize(16)
        self.light_control_button.setFont(font)
        self.light_control_button.clicked.connect(self.toggle_light)
        control_layout.addWidget(self.light_control_button)
        
        # 空调控制按钮
        self.ac_control_button = QPushButton("开关空调")
        self.ac_control_button.setFixedHeight(60)
        font = QFont()
        font.setPointSize(16)
        self.ac_control_button.setFont(font)
        self.ac_control_button.clicked.connect(self.toggle_ac)
        control_layout.addWidget(self.ac_control_button)
        
        layout.addWidget(control_group)
        
        # 批量控制区域
        batch_group = QFrame()
        batch_group.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        batch_layout = QVBoxLayout(batch_group)
        
        batch_title = QLabel("批量控制")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        batch_title.setFont(font)
        batch_layout.addWidget(batch_title)
        
        # 批量开关控制
        batch_control_layout = QHBoxLayout()
        
        self.all_on_button = QPushButton("全部开启")
        self.all_on_button.clicked.connect(self.all_on)
        batch_control_layout.addWidget(self.all_on_button)
        
        self.all_off_button = QPushButton("全部关闭")
        self.all_off_button.clicked.connect(self.all_off)
        batch_control_layout.addWidget(self.all_off_button)
        
        batch_layout.addLayout(batch_control_layout)
        
        layout.addWidget(batch_group)
        
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
        
    def toggle_motor(self):
        """
        切换电机状态
        """
        self.motor_status = not self.motor_status
        self.update_motor_status_label()
        
        # 更新按钮文本
        if self.motor_status:
            self.motor_control_button.setText("停止电机")
        else:
            self.motor_control_button.setText("启动电机")
            
        # 记录操作历史
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        status_text = "启动" if self.motor_status else "停止"
        operation = f"[{timestamp}] 电机{status_text}"
        self.operation_history.append(operation)
        
        # 限制历史记录数量
        if len(self.operation_history) > 50:
            self.operation_history.pop(0)
            
        # 更新历史记录显示
        self.update_history_display()
        
    def toggle_light(self):
        """
        切换照明状态
        """
        self.light_status = not self.light_status
        self.update_light_status_label()
        
        # 更新按钮文本
        if self.light_status:
            self.light_control_button.setText("关闭照明")
        else:
            self.light_control_button.setText("开启照明")
            
        # 记录操作历史
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        status_text = "开启" if self.light_status else "关闭"
        operation = f"[{timestamp}] 照明{status_text}"
        self.operation_history.append(operation)
        
        # 限制历史记录数量
        if len(self.operation_history) > 50:
            self.operation_history.pop(0)
            
        # 更新历史记录显示
        self.update_history_display()
        
    def toggle_ac(self):
        """
        切换空调状态
        """
        self.ac_status = not self.ac_status
        self.update_ac_status_label()
        
        # 更新按钮文本
        if self.ac_status:
            self.ac_control_button.setText("关闭空调")
        else:
            self.ac_control_button.setText("开启空调")
            
        # 记录操作历史
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        status_text = "开启" if self.ac_status else "关闭"
        operation = f"[{timestamp}] 空调{status_text}"
        self.operation_history.append(operation)
        
        # 限制历史记录数量
        if len(self.operation_history) > 50:
            self.operation_history.pop(0)
            
        # 更新历史记录显示
        self.update_history_display()
        
    def all_on(self):
        """
        全部开启
        """
        self.motor_status = True
        self.light_status = True
        self.ac_status = True
        
        self.update_motor_status_label()
        self.update_light_status_label()
        self.update_ac_status_label()
        
        # 更新按钮文本
        self.motor_control_button.setText("停止电机")
        self.light_control_button.setText("关闭照明")
        self.ac_control_button.setText("关闭空调")
        
        # 记录操作历史
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        operation = f"[{timestamp}] 全部设备开启"
        self.operation_history.append(operation)
        
        # 限制历史记录数量
        if len(self.operation_history) > 50:
            self.operation_history.pop(0)
            
        # 更新历史记录显示
        self.update_history_display()
        
    def all_off(self):
        """
        全部关闭
        """
        self.motor_status = False
        self.light_status = False
        self.ac_status = False
        
        self.update_motor_status_label()
        self.update_light_status_label()
        self.update_ac_status_label()
        
        # 更新按钮文本
        self.motor_control_button.setText("启动电机")
        self.light_control_button.setText("开启照明")
        self.ac_control_button.setText("开启空调")
        
        # 记录操作历史
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        operation = f"[{timestamp}] 全部设备关闭"
        self.operation_history.append(operation)
        
        # 限制历史记录数量
        if len(self.operation_history) > 50:
            self.operation_history.pop(0)
            
        # 更新历史记录显示
        self.update_history_display()
        
    def update_motor_status_label(self):
        """
        更新电机状态标签显示
        """
        if self.motor_status:
            self.motor_status_label.setText("电机状态: 运行中")
            self.motor_status_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.motor_status_label.setText("电机状态: 已停止")
            self.motor_status_label.setStyleSheet("color: red; font-weight: bold;")
            
    def update_light_status_label(self):
        """
        更新照明状态标签显示
        """
        if self.light_status:
            self.light_status_label.setText("照明状态: 开启")
            self.light_status_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.light_status_label.setText("照明状态: 关闭")
            self.light_status_label.setStyleSheet("color: gray; font-weight: bold;")
            
    def update_ac_status_label(self):
        """
        更新空调状态标签显示
        """
        if self.ac_status:
            self.ac_status_label.setText("空调状态: 开启")
            self.ac_status_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.ac_status_label.setText("空调状态: 关闭")
            self.ac_status_label.setStyleSheet("color: gray; font-weight: bold;")
            
    def update_history_display(self):
        """
        更新操作历史显示
        """
        self.history_list.clear()
        # 按时间倒序显示
        for operation in reversed(self.operation_history):
            item = QListWidgetItem(operation)
            if "开启" in operation or "启动" in operation or "运行" in operation:
                item.setForeground(QColor("green"))
            elif "关闭" in operation or "停止" in operation:
                item.setForeground(QColor("red"))
            else:
                item.setForeground(QColor("black"))
            self.history_list.addItem(item)
            
    def reset_button_text(self):
        """
        恢复按钮文本
        """
        if self.motor_status:
            self.motor_control_button.setText("停止电机")
        else:
            self.motor_control_button.setText("启动电机")
            
        if self.light_status:
            self.light_control_button.setText("关闭照明")
        else:
            self.light_control_button.setText("开启照明")
            
        if self.ac_status:
            self.ac_control_button.setText("关闭空调")
        else:
            self.ac_control_button.setText("开启空调")
            
    def load_sample_history(self):
        """
        加载示例操作历史
        """
        # 添加一些示例历史记录
        now = QDateTime.currentDateTime()
        self.operation_history = [
            f"[{now.addDays(-1).toString('yyyy-MM-dd hh:mm:ss')}] 电机启动",
            f"[{now.addDays(-1).addSecs(1800).toString('yyyy-MM-dd hh:mm:ss')}] 照明开启",
            f"[{now.addDays(-1).addSecs(3600*6).toString('yyyy-MM-dd hh:mm:ss')}] 空调开启",
            f"[{now.addDays(-1).addSecs(3600*6 + 1800).toString('yyyy-MM-dd hh:mm:ss')}] 全部设备关闭"
        ]
        
        self.update_history_display()


if __name__ == "__main__":
    # 测试代码
    app = QApplication(sys.argv)
    widget = WateringWidget()
    widget.show()
    sys.exit(app.exec())