#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
天气预报界面
显示未来几天的天气预报信息
"""

import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QLabel, QFrame, QApplication, QPushButton)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor


class WeatherDayWidget(QFrame):
    """
    单日天气显示小部件
    """
    def __init__(self, day="", parent=None):
        super().__init__(parent)
        self.day = day
        
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setLineWidth(2)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        
        # 日期标签
        self.day_label = QLabel(day)
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.day_label.setFont(font)
        self.day_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.day_label)
        
        # 天气图标（用文字代替）
        self.icon_label = QLabel("☀️")
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(20)
        self.icon_label.setFont(font)
        layout.addWidget(self.icon_label)
        
        # 温度范围
        self.temp_range_label = QLabel("25°/18°")
        self.temp_range_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.temp_range_label)
        
        # 天气描述
        self.desc_label = QLabel("晴")
        self.desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.desc_label)
        
    def update_weather(self, day, icon, temp_high, temp_low, description):
        """
        更新天气信息
        
        Args:
            day: 日期
            icon: 天气图标
            temp_high: 最高温度
            temp_low: 最低温度
            description: 天气描述
        """
        self.day_label.setText(day)
        self.icon_label.setText(icon)
        self.temp_range_label.setText(f"{temp_high}°/{temp_low}°")
        self.desc_label.setText(description)


class WeatherWidget(QWidget):
    """
    天气预报界面
    """
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_sample_weather()
        
    def init_ui(self):
        """
        初始化界面
        """
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # 标题
        title_label = QLabel("天气预报")
        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 当前天气
        current_group = QFrame()
        current_group.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        current_layout = QVBoxLayout(current_group)
        
        current_title = QLabel("当前天气")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        current_title.setFont(font)
        current_layout.addWidget(current_title)
        
        # 当前天气详情
        current_detail_layout = QHBoxLayout()
        
        self.current_temp = QLabel("25°C")
        font = QFont()
        font.setPointSize(36)
        font.setBold(True)
        self.current_temp.setFont(font)
        current_detail_layout.addWidget(self.current_temp)
        
        current_info_layout = QVBoxLayout()
        self.current_desc = QLabel("晴")
        self.current_desc.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.current_humidity = QLabel("湿度: 60%")
        self.current_wind = QLabel("风力: 2级")
        current_info_layout.addWidget(self.current_desc)
        current_info_layout.addWidget(self.current_humidity)
        current_info_layout.addWidget(self.current_wind)
        current_detail_layout.addLayout(current_info_layout)
        
        current_layout.addLayout(current_detail_layout)
        layout.addWidget(current_group)
        
        # 未来几天预报
        forecast_group = QFrame()
        forecast_group.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        forecast_layout = QVBoxLayout(forecast_group)
        
        forecast_title = QLabel("未来5天预报")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        forecast_title.setFont(font)
        forecast_layout.addWidget(forecast_title)
        
        # 预报网格
        self.forecast_grid = QGridLayout()
        self.forecast_grid.setSpacing(10)
        
        # 创建预报小部件
        self.forecast_widgets = []
        for i in range(5):
            widget = WeatherDayWidget()
            self.forecast_widgets.append(widget)
            row = i // 5
            col = i % 5
            self.forecast_grid.addWidget(widget, row, col)
        
        forecast_layout.addLayout(self.forecast_grid)
        layout.addWidget(forecast_group)
        
        # 更新时间
        self.update_time_label = QLabel()
        self.update_time_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.update_time_label)
        
        # 更新时间显示
        self.update_time_display()
        
    def load_sample_weather(self):
        """
        加载示例天气数据
        """
        # 更新当前天气
        self.current_temp.setText("25°C")
        self.current_desc.setText("晴")
        self.current_humidity.setText("湿度: 60%")
        self.current_wind.setText("风力: 2级")
        
        # 更新预报数据
        forecast_data = [
            ("今天", "☀️", 25, 18, "晴"),
            ("明天", "🌤️", 27, 19, "多云"),
            ("后天", "🌧️", 22, 16, "小雨"),
            ("周四", "⛅", 24, 17, "阴"),
            ("周五", "☀️", 26, 18, "晴")
        ]
        
        for i, (day, icon, high, low, desc) in enumerate(forecast_data):
            if i < len(self.forecast_widgets):
                self.forecast_widgets[i].update_weather(day, icon, high, low, desc)
                
    def update_time_display(self):
        """
        更新时间显示
        """
        from datetime import datetime
        current_time = datetime.now().strftime("更新时间: %Y-%m-%d %H:%M")
        self.update_time_label.setText(current_time)


if __name__ == "__main__":
    # 测试代码
    app = QApplication(sys.argv)
    widget = WeatherWidget()
    widget.show()
    sys.exit(app.exec())