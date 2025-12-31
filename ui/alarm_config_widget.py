#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
报警配置界面
用于设置各项环境指标的报警阈值
"""

import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFrame, 
                             QLabel, QApplication, QPushButton)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class ValueSelector(QWidget):
    """
    数值选择器组件
    用于选择报警阈值
    """
    value_changed = pyqtSignal(float)  # 数值变化信号
    
    def __init__(self, min_value, max_value, initial_value, step=1, parent=None):
        super().__init__(parent)
        self.min_value = min_value
        self.max_value = max_value
        self.current_value = initial_value
        self.step = step
        
        self.init_ui()
        
    def init_ui(self):
        """
        初始化界面
        """
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 增加按钮
        self.up_button = QPushButton("▲")
        self.up_button.setFixedHeight(30)
        font = QFont()
        font.setPointSize(10)
        self.up_button.setFont(font)
        self.up_button.clicked.connect(self.increase_value)
        layout.addWidget(self.up_button)
        
        # 数值显示
        self.value_label = QLabel(str(self.current_value))
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.value_label.setFont(font)
        layout.addWidget(self.value_label)
        
        # 减少按钮
        self.down_button = QPushButton("▼")
        self.down_button.setFixedHeight(30)
        font = QFont()
        font.setPointSize(10)
        self.down_button.setFont(font)
        self.down_button.clicked.connect(self.decrease_value)
        layout.addWidget(self.down_button)
        
    def increase_value(self):
        """
        增加数值
        """
        if self.current_value + self.step <= self.max_value:
            self.current_value += self.step
            self.value_label.setText(str(self.current_value))
            self.value_changed.emit(self.current_value)
            
    def decrease_value(self):
        """
        减少数值
        """
        if self.current_value - self.step >= self.min_value:
            self.current_value -= self.step
            self.value_label.setText(str(self.current_value))
            self.value_changed.emit(self.current_value)
            
    def get_value(self):
        """
        获取当前值
        """
        return self.current_value
        
    def set_value(self, value):
        """
        设置当前值
        
        Args:
            value: 要设置的值
        """
        if self.min_value <= value <= self.max_value:
            self.current_value = value
            self.value_label.setText(str(self.current_value))


class AlarmConfigWidget(QWidget):
    """
    报警配置界面
    """
    def __init__(self):
        super().__init__()
        
        # 报警阈值配置
        self.temp_min = 18
        self.temp_max = 28
        self.humidity_min = 30
        self.humidity_max = 70
        self.light_min = 300
        self.light_max = 1000
        self.co2_min = 400
        self.co2_max = 1000
        self.pm25_min = 0
        self.pm25_max = 35
        self.occupancy_min = 0.1
        self.occupancy_max = 0.9
        
        self.init_ui()
        self.load_default_values()
        
    def init_ui(self):
        """
        初始化界面
        """
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # 标题
        title_label = QLabel("会议室环境报警参数配置")
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 温度配置
        temp_group = QFrame()
        temp_group.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        temp_layout = QVBoxLayout(temp_group)
        
        temp_title = QLabel("温度报警范围 (°C)")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        temp_title.setFont(font)
        temp_layout.addWidget(temp_title)
        
        temp_selector_layout = QHBoxLayout()
        temp_selector_layout.addWidget(QLabel("最小值:"))
        
        self.temp_min_selector = ValueSelector(0, 50, self.temp_min, 1)
        temp_selector_layout.addWidget(self.temp_min_selector)
        
        temp_selector_layout.addWidget(QLabel("最大值:"))
        
        self.temp_max_selector = ValueSelector(0, 50, self.temp_max, 1)
        temp_selector_layout.addWidget(self.temp_max_selector)
        
        temp_layout.addLayout(temp_selector_layout)
        layout.addWidget(temp_group)
        
        # 湿度配置
        humidity_group = QFrame()
        humidity_group.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        humidity_layout = QVBoxLayout(humidity_group)
        
        humidity_title = QLabel("湿度报警范围 (%)")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        humidity_title.setFont(font)
        humidity_layout.addWidget(humidity_title)
        
        humidity_selector_layout = QHBoxLayout()
        humidity_selector_layout.addWidget(QLabel("最小值:"))
        
        self.humidity_min_selector = ValueSelector(0, 100, self.humidity_min, 1)
        humidity_selector_layout.addWidget(self.humidity_min_selector)
        
        humidity_selector_layout.addWidget(QLabel("最大值:"))
        
        self.humidity_max_selector = ValueSelector(0, 100, self.humidity_max, 1)
        humidity_selector_layout.addWidget(self.humidity_max_selector)
        
        humidity_layout.addLayout(humidity_selector_layout)
        layout.addWidget(humidity_group)
        
        # 光照配置
        light_group = QFrame()
        light_group.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        light_layout = QVBoxLayout(light_group)
        
        light_title = QLabel("光照报警范围 (lux)")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        light_title.setFont(font)
        light_layout.addWidget(light_title)
        
        light_selector_layout = QHBoxLayout()
        light_selector_layout.addWidget(QLabel("最小值:"))
        
        self.light_min_selector = ValueSelector(0, 100000, self.light_min, 1000)
        light_selector_layout.addWidget(self.light_min_selector)
        
        light_selector_layout.addWidget(QLabel("最大值:"))
        
        self.light_max_selector = ValueSelector(0, 100000, self.light_max, 1000)
        light_selector_layout.addWidget(self.light_max_selector)
        
        light_layout.addLayout(light_selector_layout)
        layout.addWidget(light_group)
        
        # 二氧化碳配置
        co2_group = QFrame()
        co2_group.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        co2_layout = QVBoxLayout(co2_group)
        
        co2_title = QLabel("二氧化碳报警范围 (ppm)")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        co2_title.setFont(font)
        co2_layout.addWidget(co2_title)
        
        co2_selector_layout = QHBoxLayout()
        co2_selector_layout.addWidget(QLabel("最小值:"))
        
        self.co2_min_selector = ValueSelector(0, 2000, self.co2_min, 10)
        co2_selector_layout.addWidget(self.co2_min_selector)
        
        co2_selector_layout.addWidget(QLabel("最大值:"))
        
        self.co2_max_selector = ValueSelector(0, 2000, self.co2_max, 10)
        co2_selector_layout.addWidget(self.co2_max_selector)
        
        co2_layout.addLayout(co2_selector_layout)
        layout.addWidget(co2_group)
        
        # PM2.5配置
        pm25_group = QFrame()
        pm25_group.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        pm25_layout = QVBoxLayout(pm25_group)
        
        pm25_title = QLabel("PM2.5报警范围 (μg/m³)")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        pm25_title.setFont(font)
        pm25_layout.addWidget(pm25_title)
        
        pm25_selector_layout = QHBoxLayout()
        pm25_selector_layout.addWidget(QLabel("最小值:"))
        
        self.pm25_min_selector = ValueSelector(0, 500, self.pm25_min, 1)
        pm25_selector_layout.addWidget(self.pm25_min_selector)
        
        pm25_selector_layout.addWidget(QLabel("最大值:"))
        
        self.pm25_max_selector = ValueSelector(0, 500, self.pm25_max, 1)
        pm25_selector_layout.addWidget(self.pm25_max_selector)
        
        pm25_layout.addLayout(pm25_selector_layout)
        layout.addWidget(pm25_group)
        
        # 会议室占用率配置
        occupancy_group = QFrame()
        occupancy_group.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        occupancy_layout = QVBoxLayout(occupancy_group)
        
        occupancy_title = QLabel("会议室占用率报警范围")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        occupancy_title.setFont(font)
        occupancy_layout.addWidget(occupancy_title)
        
        occupancy_selector_layout = QHBoxLayout()
        occupancy_selector_layout.addWidget(QLabel("最小值:"))
        
        self.occupancy_min_selector = ValueSelector(0, 1.0, self.occupancy_min, 0.01)
        occupancy_selector_layout.addWidget(self.occupancy_min_selector)
        
        occupancy_selector_layout.addWidget(QLabel("最大值:"))
        
        self.occupancy_max_selector = ValueSelector(0, 1.0, self.occupancy_max, 0.01)
        occupancy_selector_layout.addWidget(self.occupancy_max_selector)
        
        occupancy_layout.addLayout(occupancy_selector_layout)
        layout.addWidget(occupancy_group)
        
        # 保存按钮
        self.save_button = QPushButton("保存配置")
        self.save_button.setFixedHeight(40)
        font = QFont()
        font.setPointSize(12)
        self.save_button.setFont(font)
        self.save_button.clicked.connect(self.save_config)
        layout.addWidget(self.save_button)
        
        # 设置布局伸缩因子以填满窗口
        layout.addStretch(1)
        
    def load_default_values(self):
        """
        加载默认值
        """
        self.temp_min_selector.set_value(self.temp_min)
        self.temp_max_selector.set_value(self.temp_max)
        self.humidity_min_selector.set_value(self.humidity_min)
        self.humidity_max_selector.set_value(self.humidity_max)
        self.light_min_selector.set_value(self.light_min)
        self.light_max_selector.set_value(self.light_max)
        self.co2_min_selector.set_value(self.co2_min)
        self.co2_max_selector.set_value(self.co2_max)
        self.pm25_min_selector.set_value(self.pm25_min)
        self.pm25_max_selector.set_value(self.pm25_max)
        self.occupancy_min_selector.set_value(self.occupancy_min)
        self.occupancy_max_selector.set_value(self.occupancy_max)
        
    def save_config(self):
        """
        保存配置
        """
        # 获取当前设置的值
        self.temp_min = self.temp_min_selector.get_value()
        self.temp_max = self.temp_max_selector.get_value()
        self.humidity_min = self.humidity_min_selector.get_value()
        self.humidity_max = self.humidity_max_selector.get_value()
        self.light_min = self.light_min_selector.get_value()
        self.light_max = self.light_max_selector.get_value()
        self.co2_min = self.co2_min_selector.get_value()
        self.co2_max = self.co2_max_selector.get_value()
        self.pm25_min = self.pm25_min_selector.get_value()
        self.pm25_max = self.pm25_max_selector.get_value()
        self.occupancy_min = self.occupancy_min_selector.get_value()
        self.occupancy_max = self.occupancy_max_selector.get_value()
        
        # 确保最小值不大于最大值
        if self.temp_min >= self.temp_max:
            self.temp_min = self.temp_max - 1
            
        if self.humidity_min >= self.humidity_max:
            self.humidity_min = self.humidity_max - 1
            
        if self.light_min >= self.light_max:
            self.light_min = self.light_max - 1000
            
        if self.co2_min >= self.co2_max:
            self.co2_min = self.co2_max - 10
        
        if self.pm25_min >= self.pm25_max:
            self.pm25_min = self.pm25_max - 1
            
        if self.occupancy_min >= self.occupancy_max:
            self.occupancy_min = self.occupancy_max - 0.01
            
        # 更新显示
        self.load_default_values()
        
        # 显示保存成功提示
        self.save_button.setText("保存成功")
        self.button_timer.start(1000)  # 1秒后恢复按钮文本
        
    def reset_save_button_text(self):
        """
        恢复保存按钮的文本
        """
        self.save_button.setText("保存配置")


if __name__ == "__main__":
    # 测试代码
    app = QApplication(sys.argv)
    widget = AlarmConfigWidget()
    widget.show()
    sys.exit(app.exec())