#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
主窗口界面
包含环境监测、生产溯源和控制界面三个主要部分
"""

from PyQt6.QtWidgets import (QMainWindow, QTabWidget, QVBoxLayout, QWidget,
                             QApplication, QStatusBar, QLabel, QSizePolicy)
from PyQt6.QtCore import Qt, QSize
from ui.dashboard_widget import DashboardWidget
from ui.monitor_widget import MonitorWidget
from ui.history_widget import HistoryWidget
from ui.alarm_widget import AlarmWidget
from ui.planting_record_widget import PlantingRecordWidget
from ui.ventilation_widget import VentilationWidget
from ui.watering_widget import WateringWidget
from ui.alarm_config_widget import AlarmConfigWidget
from controllers.sensor_controller import SensorController, ServoController
from database.db_manager import DatabaseManager
from hardware.gpio_controller import GPIOController
from models.environment_model import EnvironmentData


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

        # 设置UI
        self.init_ui()

        # 连接信号和槽
        self.connect_signals()

        # 开始传感器监控
        self.sensor_controller.start_monitoring(3000)  # 每3秒更新一次

        # 连接GPIO控制器
        self.gpio_controller.set_max_pages(self.tab_widget.count())
        self.gpio_controller.page_changed.connect(self.on_gpio_page_changed)

    def init_ui(self):
        """
        初始化用户界面
        """
        self.setWindowTitle("秋月梨种植环境监测与生产溯源管理系统")
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
        self.monitor_widget = MonitorWidget()  # 环境监测（不含历史数据）
        self.history_widget = HistoryWidget()  # 历史数据（从环境监测拆分）
        self.planting_record_widget = PlantingRecordWidget()  # 种植记录（原天气预报+农事指导）
        self.ventilation_widget = VentilationWidget()  # 通风控制
        self.watering_widget = WateringWidget()  # 浇水控制
        self.alarm_config_widget = AlarmConfigWidget()  # 报警配置
        self.alarm_widget = AlarmWidget()  # 报警监控

        # 设置所有页面的尺寸策略为扩张填充
        self.dashboard_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.monitor_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.history_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.planting_record_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.ventilation_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.watering_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.alarm_config_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.alarm_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # 添加页面到标签页控件（只保留不需要输入的界面）
        self.tab_widget.addTab(self.dashboard_widget, "主仪表盘")
        self.tab_widget.addTab(self.monitor_widget, "环境监测")
        self.tab_widget.addTab(self.history_widget, "历史数据")
        self.tab_widget.addTab(self.planting_record_widget, "种植记录")
        self.tab_widget.addTab(self.ventilation_widget, "通风控制")
        self.tab_widget.addTab(self.watering_widget, "浇水控制")
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
                                  f"土壤湿度 {env_data.soil_moisture}%")

        # 更新仪表盘数据
        self.dashboard_widget.on_sensor_data_updated(env_data)

        # 更新环境监测页面数据
        self.monitor_widget.on_sensor_data_updated(env_data)

        # 更新报警监控数据
        self.alarm_widget.on_sensor_data_updated(env_data)

        # 更新历史数据并传递给历史数据页面
        history_data = self.sensor_controller.get_history_data(50)
        self.history_widget.update_history_table(history_data)

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
        soil_min = self.alarm_config_widget.soil_min_selector.get_value()
        soil_max = self.alarm_config_widget.soil_max_selector.get_value()

        # 更新报警监控组件的阈值
        self.alarm_widget.update_alarm_thresholds(
            temp_min, temp_max,
            humidity_min, humidity_max,
            light_min, light_max,
            soil_min, soil_max
        )

    def closeEvent(self, event):
        """
        窗口关闭事件处理
        """
        # 清理GPIO资源
        self.gpio_controller.cleanup()
        event.accept()