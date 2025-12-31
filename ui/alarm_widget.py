#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
报警监控界面
显示当前活动的报警和历史报警记录
"""

import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QLabel, QFrame, QApplication, QListWidget, 
                             QListWidgetItem, QSizePolicy, QPushButton)
from PyQt6.QtCore import Qt, QTimer, QDateTime
from PyQt6.QtGui import QFont, QColor
from models.environment_model import EnvironmentData


class AlarmItemWidget(QWidget):
    """
    报警项目显示小部件
    """
    def __init__(self, alarm_type, message, timestamp, parent=None):
        super().__init__(parent)
        
        layout = QGridLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(5)
        
        # 报警类型
        self.type_label = QLabel(alarm_type)
        font = QFont()
        font.setBold(True)
        self.type_label.setFont(font)
        self.type_label.setStyleSheet("color: red;")
        layout.addWidget(self.type_label, 0, 0)
        
        # 时间戳
        self.time_label = QLabel(timestamp)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.time_label, 0, 1)
        
        # 报警消息
        self.message_label = QLabel(message)
        self.message_label.setWordWrap(True)
        layout.addWidget(self.message_label, 1, 0, 1, 2)





class AlarmItemWidget(QWidget):
    """
    报警项目显示小部件
    """
    def __init__(self, alarm_type, message, timestamp, parent=None):
        super().__init__(parent)
        
        layout = QGridLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(5)
        
        # 报警类型
        self.type_label = QLabel(alarm_type)
        font = QFont()
        font.setBold(True)
        self.type_label.setFont(font)
        self.type_label.setStyleSheet("color: red;")
        layout.addWidget(self.type_label, 0, 0)
        
        # 时间戳
        self.time_label = QLabel(timestamp)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.time_label, 0, 1)
        
        # 报警消息
        self.message_label = QLabel(message)
        self.message_label.setWordWrap(True)
        layout.addWidget(self.message_label, 1, 0, 1, 2)


class AlarmWidget(QWidget):
    """
    报警监控界面
    """
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.alarm_history = []  # 报警历史记录
        self.active_alarms = {}  # 当前活动报警
        
        # 报警阈值配置
        self.temp_min = 18  # 会议室适宜温度范围
        self.temp_max = 28
        self.humidity_min = 30
        self.humidity_max = 70
        self.light_min = 300
        self.light_max = 1000
        self.co2_min = 400
        self.co2_max = 1000  # 会议室CO2浓度上限
        self.pm25_min = 0
        self.pm25_max = 35  # PM2.5优良标准
        self.occupancy_min = 0.1  # 会议室占用率范围
        self.occupancy_max = 0.9  # 会议室占用率范围
        
        self.init_ui()
        
        # 模拟一些初始报警
        self.simulate_initial_alarms()
        
    def init_ui(self):
        """
        初始化界面
        """
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # 标题
        title_label = QLabel("会议室环境异常报警监控")
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
        
        # 添加伸缩因子以填满窗口
        layout.addStretch(1)
        
    def update_alarm_thresholds(self, temp_min, temp_max, humidity_min, humidity_max,
                              light_min, light_max, co2_min, co2_max, pm25_min=0, pm25_max=35,
                              occupancy_min=0.1, occupancy_max=0.9):
        """
        更新报警阈值
        
        Args:
            temp_min: 温度最小值
            temp_max: 温度最大值
            humidity_min: 湿度最小值
            humidity_max: 湿度最大值
            light_min: 光照最小值
            light_max: 光照最大值
            co2_min: CO2最小值
            co2_max: CO2最大值
            pm25_min: PM2.5最小值
            pm25_max: PM2.5最大值
            occupancy_min: 会议室占用率最小值
            occupancy_max: 会议室占用率最大值
        """
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.humidity_min = humidity_min
        self.humidity_max = humidity_max
        self.light_min = light_min
        self.light_max = light_max
        self.co2_min = co2_min
        self.co2_max = co2_max
        self.pm25_min = pm25_min
        self.pm25_max = pm25_max
        self.occupancy_min = occupancy_min
        self.occupancy_max = occupancy_max
        
    def on_sensor_data_updated(self, env_data: EnvironmentData):
        """
        处理传感器数据更新并检查报警
        
        Args:
            env_data: EnvironmentData对象
        """
        self.check_alarms(env_data)
        
    def check_alarms(self, env_data: EnvironmentData):
        """
        检查报警条件
        
        Args:
            env_data: EnvironmentData对象
        """
        # 检查温度报警
        if env_data.temperature < self.temp_min:
            self.add_alarm("温度过低", f"当前温度 {env_data.temperature}°C < {self.temp_min}°C")
        elif env_data.temperature > self.temp_max:
            self.add_alarm("温度过高", f"当前温度 {env_data.temperature}°C > {self.temp_max}°C")
        else:
            self.clear_alarm("温度")
            
        # 检查湿度报警
        if env_data.humidity < self.humidity_min:
            self.add_alarm("湿度过低", f"当前湿度 {env_data.humidity}% < {self.humidity_min}%")
        elif env_data.humidity > self.humidity_max:
            self.add_alarm("湿度过高", f"当前湿度 {env_data.humidity}% > {self.humidity_max}%")
        else:
            self.clear_alarm("湿度")
            
        # 检查光照报警
        if env_data.light < self.light_min:
            self.add_alarm("光照不足", f"当前光照 {env_data.light}lux < {self.light_min}lux")
        elif env_data.light > self.light_max:
            self.add_alarm("光照过强", f"当前光照 {env_data.light}lux > {self.light_max}lux")
        else:
            self.clear_alarm("光照")
            
        # 检查二氧化碳报警
        if env_data.co2 < self.co2_min:
            self.add_alarm("CO2过低", f"当前CO2浓度 {env_data.co2}ppm < {self.co2_min}ppm")
        elif env_data.co2 > self.co2_max:
            self.add_alarm("CO2过高", f"当前CO2浓度 {env_data.co2}ppm > {self.co2_max}ppm")
        else:
            self.clear_alarm("CO2")
        
        # 检查PM2.5报警
        if env_data.pm25 > self.pm25_max:
            self.add_alarm("PM2.5超标", f"当前PM2.5浓度 {env_data.pm25}μg/m³ > {self.pm25_max}μg/m³")
        else:
            self.clear_alarm("PM2.5")
            
        # 检查占用率报警
        if env_data.occupancy < self.occupancy_min:
            self.add_alarm("会议室占用率过低", f"当前占用率 {env_data.occupancy*100:.1f}% < {self.occupancy_min*100:.1f}%")
        elif env_data.occupancy > self.occupancy_max:
            self.add_alarm("会议室占用率过高", f"当前占用率 {env_data.occupancy*100:.1f}% > {self.occupancy_max*100:.1f}%")
        else:
            self.clear_alarm("会议室占用率")
            
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
        模拟会议室环境初始报警用于测试
        """
        # 添加一些示例报警
        self.add_alarm("CO2过高", "当前CO2浓度 1200ppm > 1000ppm")
        self.add_alarm("PM2.5超标", "当前PM2.5浓度 50μg/m³ > 35μg/m³")
        
        # 更新显示
        self.update_alarm_display()


if __name__ == "__main__":
    # 测试代码
    app = QApplication(sys.argv)
    widget = AlarmWidget()
    widget.show()
    sys.exit(app.exec())