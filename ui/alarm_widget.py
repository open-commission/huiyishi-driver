#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
报警监控界面
显示环境异常报警信息
"""

import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QLabel, QFrame, QApplication, QPushButton, QListWidget,
                             QListWidgetItem)
from PyQt6.QtCore import Qt, QTimer, QDateTime
from PyQt6.QtGui import QFont, QColor, QPalette
from models.environment_model import EnvironmentData
from controllers.sensor_controller import SensorController


class AlarmItemWidget(QFrame):
    """
    报警项显示小部件
    """
    def __init__(self, alarm_type, message, timestamp, parent=None):
        super().__init__(parent)
        
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setLineWidth(1)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        
        # 报警类型
        self.type_label = QLabel(alarm_type)
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.type_label.setFont(font)
        self.type_label.setStyleSheet("color: red;")
        layout.addWidget(self.type_label)
        
        # 报警信息
        self.message_label = QLabel(message)
        self.message_label.setWordWrap(True)
        layout.addWidget(self.message_label)
        
        # 时间戳
        self.time_label = QLabel(timestamp)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        font = QFont()
        font.setPointSize(8)
        self.time_label.setFont(font)
        layout.addWidget(self.time_label)


class AlarmWidget(QWidget):
    """
    报警监控界面
    """
    def __init__(self):
        super().__init__()
        self.sensor_controller = SensorController()
        self.alarm_history = []  # 报警历史记录
        self.active_alarms = {}  # 当前活动报警
        self.init_ui()
        
        # 连接传感器数据更新信号
        self.sensor_controller.data_updated.connect(self.check_alarms)
        
        # 模拟一些初始报警
        self.simulate_initial_alarms()
        
    def init_ui(self):
        """
        初始化界面
        """
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # 标题
        title_label = QLabel("环境异常报警监控")
        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 当前报警区域
        current_group = QFrame()
        current_group.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        current_layout = QVBoxLayout(current_group)
        
        current_title = QLabel("当前活动报警")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        current_title.setFont(font)
        current_layout.addWidget(current_title)
        
        self.current_alarms_list = QListWidget()
        current_layout.addWidget(self.current_alarms_list)
        
        layout.addWidget(current_group)
        
        # 报警历史区域
        history_group = QFrame()
        history_group.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        history_layout = QVBoxLayout(history_group)
        
        history_title = QLabel("报警历史记录")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        history_title.setFont(font)
        history_layout.addWidget(history_title)
        
        self.alarm_history_list = QListWidget()
        history_layout.addWidget(self.alarm_history_list)
        
        layout.addWidget(history_group)
        
        # 控制按钮
        button_layout = QHBoxLayout()
        
        self.acknowledge_button = QPushButton("确认报警")
        self.acknowledge_button.clicked.connect(self.acknowledge_current_alarms)
        button_layout.addWidget(self.acknowledge_button)
        
        self.clear_history_button = QPushButton("清除历史")
        self.clear_history_button.clicked.connect(self.clear_alarm_history)
        button_layout.addWidget(self.clear_history_button)
        
        layout.addLayout(button_layout)
        
    def check_alarms(self, env_data: EnvironmentData):
        """
        检查环境数据并生成报警
        
        Args:
            env_data: EnvironmentData对象
        """
        # 检查温度报警
        if env_data.temperature < 10:
            self.add_alarm("温度过低", f"当前温度 {env_data.temperature}°C < 10°C")
        elif env_data.temperature > 35:
            self.add_alarm("温度过高", f"当前温度 {env_data.temperature}°C > 35°C")
        else:
            self.clear_alarm("温度")
            
        # 检查湿度报警
        if env_data.humidity < 40:
            self.add_alarm("湿度过低", f"当前湿度 {env_data.humidity}% < 40%")
        elif env_data.humidity > 80:
            self.add_alarm("湿度过高", f"当前湿度 {env_data.humidity}% > 80%")
        else:
            self.clear_alarm("湿度")
            
        # 检查光照报警
        light_klux = env_data.light / 1000
        if light_klux < 5:
            self.add_alarm("光照不足", f"当前光照 {light_klux}k lux < 5k lux")
        elif light_klux > 50:
            self.add_alarm("光照过强", f"当前光照 {light_klux}k lux > 50k lux")
        else:
            self.clear_alarm("光照")
            
        # 检查土壤湿度报警
        if env_data.soil_moisture < 30:
            self.add_alarm("土壤过干", f"当前土壤湿度 {env_data.soil_moisture}% < 30%")
        elif env_data.soil_moisture > 80:
            self.add_alarm("土壤过湿", f"当前土壤湿度 {env_data.soil_moisture}% > 80%")
        else:
            self.clear_alarm("土壤湿度")
            
        # 更新显示
        self.update_alarm_display()
        
    def add_alarm(self, alarm_type, message):
        """
        添加报警
        
        Args:
            alarm_type: 报警类型
            message: 报警信息
        """
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        
        # 如果报警已存在，则更新时间戳
        if alarm_type in self.active_alarms:
            self.active_alarms[alarm_type]["timestamp"] = timestamp
        else:
            # 添加新报警
            alarm_info = {
                "type": alarm_type,
                "message": message,
                "timestamp": timestamp
            }
            self.active_alarms[alarm_type] = alarm_info
            
            # 添加到历史记录
            self.alarm_history.append(alarm_info)
            if len(self.alarm_history) > 100:  # 限制历史记录数量
                self.alarm_history.pop(0)
        
    def clear_alarm(self, alarm_type_prefix):
        """
        清除指定类型的报警
        
        Args:
            alarm_type_prefix: 报警类型前缀
        """
        # 找到并移除匹配的报警
        keys_to_remove = []
        for key in self.active_alarms:
            if key.startswith(alarm_type_prefix):
                keys_to_remove.append(key)
                
        for key in keys_to_remove:
            del self.active_alarms[key]
            
    def update_alarm_display(self):
        """
        更新报警显示
        """
        # 更新当前报警列表
        self.current_alarms_list.clear()
        for alarm_info in self.active_alarms.values():
            item = QListWidgetItem()
            widget = AlarmItemWidget(
                alarm_info["type"],
                alarm_info["message"],
                alarm_info["timestamp"]
            )
            item.setSizeHint(widget.sizeHint())
            self.current_alarms_list.addItem(item)
            self.current_alarms_list.setItemWidget(item, widget)
            
        # 更新历史记录列表
        self.alarm_history_list.clear()
        # 按时间倒序显示历史记录
        for alarm_info in reversed(self.alarm_history):
            item = QListWidgetItem()
            widget = AlarmItemWidget(
                alarm_info["type"],
                alarm_info["message"],
                alarm_info["timestamp"]
            )
            item.setSizeHint(widget.sizeHint())
            self.alarm_history_list.addItem(item)
            self.alarm_history_list.setItemWidget(item, widget)
            
    def acknowledge_current_alarms(self):
        """
        确认当前报警
        """
        self.active_alarms.clear()
        self.update_alarm_display()
        
    def clear_alarm_history(self):
        """
        清除报警历史
        """
        self.alarm_history.clear()
        self.update_alarm_display()
        
    def simulate_initial_alarms(self):
        """
        模拟初始报警用于测试
        """
        # 添加一些示例报警
        self.add_alarm("温度过高", "当前温度 36.5°C > 35°C")
        self.add_alarm("湿度过低", "当前湿度 35% < 40%")
        
        # 更新显示
        self.update_alarm_display()


if __name__ == "__main__":
    # 测试代码
    app = QApplication(sys.argv)
    widget = AlarmWidget()
    widget.show()
    sys.exit(app.exec())