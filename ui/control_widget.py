#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
设备控制界面
用于控制舵机等设备
"""

import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QGroupBox, QProgressBar, QApplication)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QColor, QPalette


class ControlWidget(QWidget):
    """
    设备控制界面
    """
    # 定义信号
    servo_toggle_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.servo_status = False  # False表示关闭，True表示开启
        self.init_ui()
        
    def init_ui(self):
        """
        初始化界面
        """
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # 标题
        title_label = QLabel("设备控制系统")
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 创建舵机组件
        servo_group = QGroupBox("舵机控制")
        servo_layout = QVBoxLayout(servo_group)
        
        # 舵机状态显示
        self.servo_status_label = QLabel("舵机状态: 已关闭")
        font = QFont()
        font.setPointSize(14)
        self.servo_status_label.setFont(font)
        self.servo_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        servo_layout.addWidget(self.servo_status_label)
        
        # 更新状态标签颜色
        self.update_servo_status_label()
        
        # 舵机控制按钮
        self.servo_button = QPushButton("启动舵机")
        self.servo_button.setFixedHeight(50)
        font = QFont()
        font.setPointSize(12)
        self.servo_button.setFont(font)
        self.servo_button.clicked.connect(self.on_servo_button_clicked)
        servo_layout.addWidget(self.servo_button)
        
        layout.addWidget(servo_group)
        
        # 创建进度条组件（模拟设备运行状态）
        progress_group = QGroupBox("设备运行状态")
        progress_layout = QVBoxLayout(progress_group)
        
        # 进度条标签
        progress_label = QLabel("设备运行进度:")
        progress_layout.addWidget(progress_label)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        progress_layout.addWidget(self.progress_bar)
        
        layout.addWidget(progress_group)
        
        # 创建系统信息组件
        info_group = QGroupBox("系统信息")
        info_layout = QVBoxLayout(info_group)
        
        info_text = """
        <html>
        <body>
        <p><b>设备控制说明:</b></p>
        <ul>
        <li>点击"启动舵机"按钮可切换舵机开关状态</li>
        <li>舵机开启后会自动执行预设动作</li>
        <li>设备运行进度显示当前工作进度</li>
        <li>紧急情况下可通过断电方式停止设备</li>
        </ul>
        <p><b>注意事项:</b></p>
        <ul>
        <li>请勿频繁切换舵机状态</li>
        <li>定期检查设备运行情况</li>
        <li>如发现异常请及时联系技术人员</li>
        </ul>
        </body>
        </html>
        """
        
        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        info_layout.addWidget(info_label)
        
        layout.addWidget(info_group)
        
        # 设置布局伸缩因子
        layout.setStretch(0, 0)  # 标题
        layout.setStretch(1, 0)  # 舵机组件
        layout.setStretch(2, 0)  # 进度条组件
        layout.setStretch(3, 1)  # 信息组件
        
        # 启动定时器模拟进度更新
        self.progress_timer = QTimer(self)
        self.progress_timer.timeout.connect(self.update_progress)
        self.progress_value = 0
        self.progress_timer.start(100)  # 每100毫秒更新一次
        
    def on_servo_button_clicked(self):
        """
        处理舵机按钮点击事件
        """
        # 发出信号请求切换舵机状态
        self.servo_toggle_requested.emit()
        
    def update_servo_status(self, is_active: bool):
        """
        更新舵机状态显示
        
        Args:
            is_active: 舵机是否激活
        """
        self.servo_status = is_active
        self.update_servo_status_label()
        
        # 更新按钮文本
        if is_active:
            self.servo_button.setText("关闭舵机")
        else:
            self.servo_button.setText("启动舵机")
            
    def update_servo_status_label(self):
        """
        更新舵机状态标签显示和颜色
        """
        if self.servo_status:
            self.servo_status_label.setText("舵机状态: 运行中")
            # 设置为绿色
            palette = self.servo_status_label.palette()
            palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 150, 0))
            self.servo_status_label.setPalette(palette)
        else:
            self.servo_status_label.setText("舵机状态: 已关闭")
            # 设置为红色
            palette = self.servo_status_label.palette()
            palette.setColor(QPalette.ColorRole.WindowText, QColor(200, 0, 0))
            self.servo_status_label.setPalette(palette)
            
        # 确保调色板生效
        self.servo_status_label.setAutoFillBackground(True)
        
    def update_progress(self):
        """
        更新进度条
        """
        if self.servo_status:
            self.progress_value = (self.progress_value + 1) % 101
            self.progress_bar.setValue(self.progress_value)
        else:
            self.progress_bar.setValue(0)
            self.progress_value = 0


if __name__ == "__main__":
    # 测试代码
    app = QApplication(sys.argv)
    widget = ControlWidget()
    widget.show()
    sys.exit(app.exec())