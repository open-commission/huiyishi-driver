#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
主窗口界面
包含环境监测、生产溯源和控制界面三个主要部分
"""

from PyQt6.QtWidgets import (QMainWindow, QTabWidget, QVBoxLayout, QWidget, 
                             QApplication, QStatusBar, QLabel)
from PyQt6.QtCore import Qt
from ui.dashboard_widget import DashboardWidget
from ui.monitor_widget import MonitorWidget
from ui.alarm_widget import AlarmWidget
from ui.weather_widget import WeatherWidget
from ui.farming_widget import FarmingWidget
from ui.statistics_widget import StatisticsWidget
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
        # 设置窗口为全屏
        self.showFullScreen()
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建标签页控件
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # 创建各个功能页面
        self.dashboard_widget = DashboardWidget()    # 主仪表盘
        self.monitor_widget = MonitorWidget()        # 环境监测
        self.alarm_widget = AlarmWidget()            # 报警监控
        self.weather_widget = WeatherWidget()        # 天气预报
        self.farming_widget = FarmingWidget()        # 农事指导
        self.statistics_widget = StatisticsWidget()  # 统计分析
        # 移除生产溯源和设备控制界面
        
        # 添加页面到标签页控件（只保留不需要输入的界面）
        self.tab_widget.addTab(self.dashboard_widget, "主仪表盘")
        self.tab_widget.addTab(self.monitor_widget, "环境监测")
        self.tab_widget.addTab(self.alarm_widget, "报警监控")
        self.tab_widget.addTab(self.weather_widget, "天气预报")
        self.tab_widget.addTab(self.farming_widget, "农事指导")
        self.tab_widget.addTab(self.statistics_widget, "统计分析")
        
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
        
    def closeEvent(self, event):
        """
        窗口关闭事件处理
        """
        # 清理GPIO资源
        self.gpio_controller.cleanup()
        event.accept()