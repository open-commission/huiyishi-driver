#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
主窗口界面
包含会议室环境监测、会议室控制和管理界面三个主要部分
"""

from PyQt6.QtWidgets import (QMainWindow, QTabWidget, QVBoxLayout, QWidget,
                             QApplication, QStatusBar, QLabel, QSizePolicy)
from PyQt6.QtCore import Qt, QSize
from ui.dashboard_widget import DashboardWidget
from ui.monitor_widget import MonitorWidget
from ui.history_widget import HistoryWidget
from ui.alarm_widget import AlarmWidget
from ui.planting_record_widget import PlantingRecordWidget  # 会议室记录
from ui.ventilation_widget import VentilationWidget
from ui.watering_widget import WateringWidget
from ui.alarm_config_widget import AlarmConfigWidget
from controllers.sensor_controller import SensorController, ServoController
from database.db_manager import DatabaseManager
from hardware.gpio_controller import GPIOController
from hardware.ir_controller import IRController
from models.environment_model import EnvironmentData
from remote_config import PAGE_MAPPING


class MainWindow(QMainWindow):
    """
    主窗口类
    """

    def __init__(self):
        super().__init__()

        # 初始化控制器和数据模型
        self.sensor_controller = SensorController()
        self.servo_controller = ServoController()
        self.database = DatabaseManager()
        self.gpio_controller = GPIOController()
        self.ir_controller = IRController()

        # 设置UI
        self.init_ui()

        # 连接信号和槽
        self.connect_signals()

        # 开始传感器监控
        self.sensor_controller.start_monitoring(3000)  # 每3秒更新一次

        # 连接GPIO控制器
        self.gpio_controller.set_max_pages(self.tab_widget.count())
        self.gpio_controller.page_changed.connect(self.on_gpio_page_changed)

        # 启动红外事件监听
        self.ir_controller.ir_event_logged.connect(self.on_ir_event_logged)
        self.ir_controller.ir_key_pressed.connect(self.on_ir_key_pressed)
        self.ir_controller.start_ir_monitoring()

    def init_ui(self):
        """
        初始化用户界面
        """
        self.setWindowTitle("基于esp8266与H618的多功能会议室管理终端")
        # 设置窗口大小
        self.resize(1024, 768)
        self.setMinimumSize(QSize(800, 600))

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)  # 移除边距

        # 创建标签页控件
        self.tab_widget = QTabWidget()
        self.tab_widget.setDocumentMode(True)  # 使用文档模式以获得更好的外观
        main_layout.addWidget(self.tab_widget)

        # 创建各个功能页面
        self.dashboard_widget = DashboardWidget()  # 主仪表盘
        self.monitor_widget = MonitorWidget()  # 会议室环境监测（不含历史数据）
        self.history_widget = HistoryWidget()  # 历史数据（从环境监测拆分）
        self.meeting_record_widget = PlantingRecordWidget()  # 会议室记录
        self.room_control_widget = VentilationWidget()  # 会议室控制（类名保持不变以避免重构）
        self.device_control_widget = WateringWidget()  # 设备控制（类名保持不变以避免重构）
        self.alarm_config_widget = AlarmConfigWidget()  # 报警配置
        self.alarm_widget = AlarmWidget()  # 报警监控

        # 设置所有页面的尺寸策略为扩张填充
        self.dashboard_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.monitor_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.history_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.meeting_record_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.room_control_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.device_control_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.alarm_config_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.alarm_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # 添加页面到标签页控件（只保留不需要输入的界面）
        self.tab_widget.addTab(self.dashboard_widget, "主仪表盘")
        self.tab_widget.addTab(self.monitor_widget, "会议室环境")
        self.tab_widget.addTab(self.history_widget, "历史数据")
        self.tab_widget.addTab(self.meeting_record_widget, "会议室记录")
        self.tab_widget.addTab(self.room_control_widget, "会议室控制")
        self.tab_widget.addTab(self.device_control_widget, "设备控制")
        self.tab_widget.addTab(self.alarm_config_widget, "报警配置")
        self.tab_widget.addTab(self.alarm_widget, "报警监控")

        # 连接报警配置保存按钮
        self.alarm_config_widget.save_button.clicked.connect(self.on_alarm_config_saved)

        # 创建状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # 添加状态栏标签
        self.status_label = QLabel("系统就绪")
        self.status_bar.addWidget(self.status_label)

    def connect_signals(self):
        """
        连接信号和槽
        """
        # 连接传感器数据更新信号
        self.sensor_controller.data_updated.connect(self.on_sensor_data_updated)

        # 连接舵机状态变化信号
        self.servo_controller.status_changed.connect(self.on_servo_status_changed)

    def on_sensor_data_updated(self, env_data: EnvironmentData):
        """
        处理传感器数据更新

        Args:
            env_data: EnvironmentData对象
        """
        # 更新状态栏
        self.status_label.setText(f"环境数据更新: 温度 {env_data.temperature}°C, "
                                  f"湿度 {env_data.humidity}%, "
                                  f"光照 {env_data.light}lux, "
                                  f"CO2 {env_data.co2}ppm, "
                                  f"PM2.5 {env_data.pm25}μg/m³, "
                                  f"占用率 {env_data.occupancy*100:.1f}%")

        # 安全更新仪表盘数据
        try:
            if self.dashboard_widget:
                self.dashboard_widget.on_sensor_data_updated(env_data)
        except RuntimeError:
            # 组件可能已被删除，忽略错误
            pass

        # 更新环境监测页面数据
        try:
            if self.monitor_widget:
                self.monitor_widget.on_sensor_data_updated(env_data)
        except RuntimeError:
            pass

        # 更新报警监控数据
        try:
            if self.alarm_widget:
                self.alarm_widget.on_sensor_data_updated(env_data)
        except RuntimeError:
            pass

        # 更新历史数据并传递给历史数据页面
        try:
            if self.history_widget:
                history_data = self.sensor_controller.get_history_data(50)
                self.history_widget.update_history_table(history_data)
        except RuntimeError:
            pass

    def on_servo_status_changed(self, is_active):
        """
        处理舵机状态变化

        Args:
            is_active: 舵机是否激活
        """
        # 更新状态栏
        status_text = "舵机已开启" if is_active else "舵机已关闭"
        self.status_label.setText(status_text)

    def on_gpio_page_changed(self, page_index):
        """
        处理GPIO页面切换请求

        Args:
            page_index: 页面索引
        """
        self.tab_widget.setCurrentIndex(page_index)

    def on_alarm_config_saved(self):
        """
        处理报警配置保存事件
        """
        # 获取报警配置参数
        temp_min = self.alarm_config_widget.temp_min_selector.get_value()
        temp_max = self.alarm_config_widget.temp_max_selector.get_value()
        humidity_min = self.alarm_config_widget.humidity_min_selector.get_value()
        humidity_max = self.alarm_config_widget.humidity_max_selector.get_value()
        light_min = self.alarm_config_widget.light_min_selector.get_value()
        light_max = self.alarm_config_widget.light_max_selector.get_value()
        co2_min = self.alarm_config_widget.co2_min_selector.get_value()
        co2_max = self.alarm_config_widget.co2_max_selector.get_value()

        # 更新报警监控组件的阈值
        occupancy_min = self.alarm_config_widget.occupancy_min_selector.get_value()
        occupancy_max = self.alarm_config_widget.occupancy_max_selector.get_value()
        
        self.alarm_widget.update_alarm_thresholds(
            temp_min, temp_max,
            humidity_min, humidity_max,
            light_min, light_max,
            co2_min, co2_max,
            occupancy_min=occupancy_min,
            occupancy_max=occupancy_max
        )

    def on_ir_event_logged(self, log_msg):
        """
        处理红外事件日志
        
        Args:
            log_msg: 日志消息
        """
        print(log_msg)  # 在控制台输出红外事件
        # 可以根据需要添加到状态栏或其他UI组件
        self.status_label.setText(f"红外事件: {log_msg[-50:]}..." if len(log_msg) > 50 else f"红外事件: {log_msg}")

    def on_ir_key_pressed(self, keycode):
        """
        处理红外按键按下事件
        
        Args:
            keycode: 按键码
        """
        print(f"红外按键按下: {keycode}")
        # 根据按键码切换到对应的页面
        
        if keycode in PAGE_MAPPING:
            page_name = PAGE_MAPPING[keycode]
            # 根据页面名称找到对应的标签页索引并切换
            for i in range(self.tab_widget.count()):
                if self.tab_widget.tabText(i) == self.get_tab_text_by_page_name(page_name):
                    self.tab_widget.setCurrentIndex(i)
                    self.status_label.setText(f"切换到: {self.tab_widget.tabText(i)}")
                    break

    def get_tab_text_by_page_name(self, page_name):
        """
        根据页面名称获取标签页文本
        
        Args:
            page_name: 页面名称
            
        Returns:
            str: 标签页文本
        """
        page_name_mapping = {
            'meeting_dashboard': '主仪表盘',
            'meeting_monitor': '会议室环境',
            'meeting_history': '历史数据',
            'meeting_control': '会议室控制',
            'field_dashboard': '主仪表盘',
            'field_monitor': '会议室环境',
            'field_history': '历史数据',
            'device_control': '设备控制',
            'alarm_config': '报警配置',
            'alarm_monitor': '报警监控',
            'main_dashboard': '主仪表盘',
        }
        return page_name_mapping.get(page_name, '主仪表盘')

    def closeEvent(self, event):
        """
        窗口关闭事件处理
        """
        # 清理GPIO资源
        self.gpio_controller.cleanup()
        # 清理红外控制器资源
        self.ir_controller.cleanup()
        event.accept()