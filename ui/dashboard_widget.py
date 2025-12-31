#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
仪表盘显示组件
显示当前环境数据的综合视图
"""

import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QLabel, QFrame, QApplication, QProgressBar)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor, QPalette
from models.environment_model import EnvironmentData


class DashboardValueWidget(QFrame):
    """
    仪表盘数值显示小部件
    """
    def __init__(self, title, unit="", parent=None):
        super().__init__(parent)
        self.title = title
        self.unit = unit
        
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setLineWidth(2)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        
        # 标题标签
        self.title_label = QLabel(title)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.title_label.setFont(font)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)
        
        # 数值标签
        self.value_label = QLabel("0.00")
        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.value_label.setFont(font)
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.value_label)
        
        # 单位标签
        self.unit_label = QLabel(unit)
        font = QFont()
        font.setPointSize(12)
        self.unit_label.setFont(font)
        self.unit_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.unit_label)
        
    def update_value(self, value):
        """
        更新显示的数值
        
        Args:
            value: 新的数值
        """
        self.value_label.setText(f"{value:.1f}")


class StatusIndicator(QWidget):
    """
    状态指示器
    """
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.title = title
        self.status = False  # False=正常, True=异常
        
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        
        # 标题
        self.title_label = QLabel(title)
        font = QFont()
        font.setPointSize(12)
        self.title_label.setFont(font)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)
        
        # 状态指示灯
        self.indicator = QLabel()
        self.indicator.setFixedSize(30, 30)
        self.indicator.setStyleSheet("background-color: red; border-radius: 15px;")
        self.indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.indicator, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # 状态文本
        self.status_label = QLabel("正常")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        self.update_status(False)
        
    def update_status(self, is_abnormal):
        """
        更新状态显示
        
        Args:
            is_abnormal: 是否异常 (True=异常, False=正常)
        """
        self.status = is_abnormal
        if is_abnormal:
            self.indicator.setStyleSheet("background-color: red; border-radius: 15px;")
            self.status_label.setText("异常")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
        else:
            self.indicator.setStyleSheet("background-color: green; border-radius: 15px;")
            self.status_label.setText("正常")
            self.status_label.setStyleSheet("color: green; font-weight: bold;")


class DashboardWidget(QWidget):
    """
    仪表盘显示组件
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.init_ui()
        self.init_timer()
        
    def init_ui(self):
        """
        初始化界面
        """
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # 标题
        title_label = QLabel("会议室环境监控仪表盘")
        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 指标显示区域
        metrics_group = QFrame()
        metrics_group.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        metrics_layout = QGridLayout(metrics_group)
        metrics_layout.setSpacing(20)
        
        # 温度
        self.temp_widget = DashboardValueWidget("温度", "°C")
        metrics_layout.addWidget(self.temp_widget, 0, 0)
        
        # 湿度
        self.humidity_widget = DashboardValueWidget("湿度", "%")
        metrics_layout.addWidget(self.humidity_widget, 0, 1)
        
        # 光照
        self.light_widget = DashboardValueWidget("光照", "klx")
        metrics_layout.addWidget(self.light_widget, 1, 0)
        
        # 会议室占用率
        self.occupancy_widget = DashboardValueWidget("会议室占用率", "%")
        metrics_layout.addWidget(self.occupancy_widget, 1, 1)
        
        layout.addLayout(metrics_layout)
        
        # 状态指示器
        status_layout = QHBoxLayout()
        status_layout.setSpacing(30)
        
        self.temp_status = StatusIndicator("温度状态")
        self.humidity_status = StatusIndicator("湿度状态")
        self.light_status = StatusIndicator("光照状态")
        self.occupancy_status = StatusIndicator("会议室占用率状态")
        
        status_layout.addWidget(self.temp_status)
        status_layout.addWidget(self.humidity_status)
        status_layout.addWidget(self.light_status)
        status_layout.addWidget(self.occupancy_status)
        
        layout.addLayout(status_layout)
        
        # 进度条显示
        progress_layout = QVBoxLayout()
        progress_layout.setSpacing(10)
        
        # 温度进度条
        temp_progress_layout = QHBoxLayout()
        temp_progress_layout.addWidget(QLabel("温度:"))
        self.temp_progress = QProgressBar()
        self.temp_progress.setRange(0, 40)  # 0-40度
        self.temp_progress.setValue(25)
        temp_progress_layout.addWidget(self.temp_progress)
        progress_layout.addLayout(temp_progress_layout)
        
        # 湿度进度条
        humidity_progress_layout = QHBoxLayout()
        humidity_progress_layout.addWidget(QLabel("湿度:"))
        self.humidity_progress = QProgressBar()
        self.humidity_progress.setRange(0, 100)  # 0-100%
        self.humidity_progress.setValue(60)
        humidity_progress_layout.addWidget(self.humidity_progress)
        progress_layout.addLayout(humidity_progress_layout)
        
        # 光照进度条
        light_progress_layout = QHBoxLayout()
        light_progress_layout.addWidget(QLabel("光照:"))
        self.light_progress = QProgressBar()
        self.light_progress.setRange(0, 100)  # 0-100k lux
        self.light_progress.setValue(50)
        light_progress_layout.addWidget(self.light_progress)
        progress_layout.addLayout(light_progress_layout)
        
        # 会议室占用率进度条
        occupancy_progress_layout = QHBoxLayout()
        occupancy_progress_layout.addWidget(QLabel("会议室占用率:"))
        self.occupancy_progress = QProgressBar()
        self.occupancy_progress.setRange(0, 100)  # 0-100%
        self.occupancy_progress.setValue(0)
        occupancy_progress_layout.addWidget(self.occupancy_progress)
        progress_layout.addLayout(occupancy_progress_layout)
        
        layout.addLayout(progress_layout)
        
        # 时间显示
        self.time_label = QLabel()
        font = QFont()
        font.setPointSize(14)
        self.time_label.setFont(font)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.time_label)
        
        # 更新时间显示
        self.update_time_display()
        
        # 添加伸缩因子以填满窗口
        layout.addStretch(1)
        
    def init_timer(self):
        """
        初始化定时器
        """
        self.time_timer = QTimer(self)
        self.time_timer.timeout.connect(self.update_time_display)
        self.time_timer.start(1000)  # 每秒更新一次时间
        
    def on_sensor_data_updated(self, env_data: EnvironmentData):
        """
        处理传感器数据更新
        
        Args:
            env_data: EnvironmentData对象
        """
        # 更新数值显示
        self.temp_widget.update_value(env_data.temperature)
        self.humidity_widget.update_value(env_data.humidity)
        self.light_widget.update_value(env_data.light / 1000)  # 转换为k lux
        self.occupancy_widget.update_value(env_data.occupancy * 100)  # 转换为百分比
        
        # 更新进度条
        self.temp_progress.setValue(int(env_data.temperature))
        self.humidity_progress.setValue(int(env_data.humidity))
        self.light_progress.setValue(int(env_data.light / 1000))  # 转换为k lux
        self.occupancy_progress.setValue(int(env_data.occupancy * 100))
        
        # 更新状态指示器
        self.temp_status.update_status(env_data.temperature < 18 or env_data.temperature > 28)  # 适宜温度范围
        self.humidity_status.update_status(env_data.humidity < 30 or env_data.humidity > 70)  # 适宜湿度范围
        self.light_status.update_status(env_data.light < 300 or env_data.light > 100000)  # 适宜光照范围
        self.occupancy_status.update_status(env_data.occupancy < 0.1 or env_data.occupancy > 0.9)  # 会议室占用率异常
        
    def update_time_display(self):
        """
        更新时间显示
        """
        from datetime import datetime
        current_time = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        self.time_label.setText(current_time)


if __name__ == "__main__":
    # 测试代码
    app = QApplication(sys.argv)
    widget = DashboardWidget()
    widget.show()
    sys.exit(app.exec())