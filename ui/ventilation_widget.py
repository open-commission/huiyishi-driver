#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
会议室控制界面
用于控制会议室设备并记录操作历史
"""

import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QFrame, QApplication, QPushButton, QListWidget,
                             QListWidgetItem, QSizePolicy, QLineEdit, QGroupBox)
from PyQt6.QtCore import Qt, QDateTime, QTimer
from PyQt6.QtGui import QFont, QColor


class VentilationWidget(QWidget):
    """
    会议室控制界面
    """
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.servo_status = False  # 舵机状态 False表示关闭，True表示开启
        self.rfid_status = False   # RFID状态
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
        title_label = QLabel("会议室控制")
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
        
        # 舵机状态
        self.servo_status_label = QLabel("舵机状态: 未激活")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.servo_status_label.setFont(font)
        self.servo_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.update_servo_status_label()
        status_layout.addWidget(self.servo_status_label)
        
        # RFID状态
        self.rfid_status_label = QLabel("RFID读取: 未激活")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.rfid_status_label.setFont(font)
        self.rfid_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.update_rfid_status_label()
        status_layout.addWidget(self.rfid_status_label)
        
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
        
        # 舵机控制按钮
        self.servo_control_button = QPushButton("激活舵机")
        self.servo_control_button.setFixedHeight(60)
        font = QFont()
        font.setPointSize(16)
        self.servo_control_button.setFont(font)
        self.servo_control_button.clicked.connect(self.toggle_servo)
        control_layout.addWidget(self.servo_control_button)
        
        # RFID模拟输入区域
        rfid_group = QGroupBox("RFID读取")
        rfid_layout = QVBoxLayout(rfid_group)
        
        self.rfid_input = QLineEdit()
        self.rfid_input.setPlaceholderText("输入RFID卡号或点击按钮模拟读取")
        rfid_layout.addWidget(self.rfid_input)
        
        self.rfid_read_button = QPushButton("模拟RFID读取")
        self.rfid_read_button.clicked.connect(self.simulate_rfid_read)
        rfid_layout.addWidget(self.rfid_read_button)
        
        control_layout.addWidget(rfid_group)
        
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
        
    def toggle_servo(self):
        """
        切换舵机状态
        """
        self.servo_status = not self.servo_status
        self.update_servo_status_label()
        
        # 更新按钮文本
        if self.servo_status:
            self.servo_control_button.setText("关闭舵机")
        else:
            self.servo_control_button.setText("激活舵机")
            
        # 记录操作历史
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        status_text = "激活" if self.servo_status else "关闭"
        operation = f"[{timestamp}] 舵机{status_text}"
        self.operation_history.append(operation)
        
        # 限制历史记录数量
        if len(self.operation_history) > 50:
            self.operation_history.pop(0)
            
        # 更新历史记录显示
        self.update_history_display()
        
    def simulate_rfid_read(self):
        """
        模拟RFID读取
        """
        # 模拟RFID读取
        rfid_code = self.rfid_input.text()
        if not rfid_code:
            # 如果没有输入，生成一个模拟的RFID码
            import random
            rfid_code = f"RFID_{random.randint(1000, 9999)}"
        
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        operation = f"[{timestamp}] RFID读取: {rfid_code}"
        self.operation_history.append(operation)
        
        # 限制历史记录数量
        if len(self.operation_history) > 50:
            self.operation_history.pop(0)
            
        # 更新历史记录显示
        self.update_history_display()
        
        # 显示RFID读取成功提示
        self.rfid_read_button.setText("读取成功")
        self.button_timer.timeout.connect(lambda: setattr(self.rfid_read_button, 'text', '模拟RFID读取'))
        self.button_timer.start(1000)  # 1秒后恢复按钮文本
        
    def update_servo_status_label(self):
        """
        更新舵机状态标签显示
        """
        if self.servo_status:
            self.servo_status_label.setText("舵机状态: 运行中")
            self.servo_status_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.servo_status_label.setText("舵机状态: 已停止")
            self.servo_status_label.setStyleSheet("color: red; font-weight: bold;")
            
    def update_rfid_status_label(self):
        """
        更新RFID状态标签显示
        """
        if self.rfid_status:
            self.rfid_status_label.setText("RFID读取: 活跃")
            self.rfid_status_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.rfid_status_label.setText("RFID读取: 未激活")
            self.rfid_status_label.setStyleSheet("color: gray; font-weight: bold;")
            
    def update_history_display(self):
        """
        更新操作历史显示
        """
        self.history_list.clear()
        # 按时间倒序显示
        for operation in reversed(self.operation_history):
            item = QListWidgetItem(operation)
            if "激活" in operation or "运行" in operation or "读取" in operation:
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
        if self.servo_status:
            self.servo_control_button.setText("关闭舵机")
        else:
            self.servo_control_button.setText("激活舵机")
            
        # 恢复RFID按钮文本
        self.rfid_read_button.setText("模拟RFID读取")
        
    def load_sample_history(self):
        """
        加载示例操作历史
        """
        # 添加一些示例历史记录
        now = QDateTime.currentDateTime()
        self.operation_history = [
            f"[{now.addDays(-1).toString('yyyy-MM-dd hh:mm:ss')}] 舵机激活",
            f"[{now.addDays(-1).addSecs(3600*4).toString('yyyy-MM-dd hh:mm:ss')}] RFID读取: RFID_1234",
            f"[{now.addDays(-1).addSecs(3600*8).toString('yyyy-MM-dd hh:mm:ss')}] 舵机关闭",
            f"[{now.addDays(-1).addSecs(3600*12).toString('yyyy-MM-dd hh:mm:ss')}] RFID读取: RFID_5678"
        ]
        
        self.update_history_display()


if __name__ == "__main__":
    # 测试代码
    app = QApplication(sys.argv)
    widget = VentilationWidget()
    widget.show()
    sys.exit(app.exec())