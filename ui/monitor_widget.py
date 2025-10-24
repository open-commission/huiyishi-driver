#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
环境监测界面组件
显示实时环境数据和可视化图表
"""

import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QLabel, QFrame, QApplication, QPushButton, QTableWidget,
                             QTableWidgetItem, QHeaderView, QGroupBox, QTabWidget)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor
from ui.chart_widget import ChartWidget
from ui.bar_chart_widget import BarChartWidget
from models.environment_model import EnvironmentData


class DataDisplayWidget(QFrame):
    """
    数据显示小部件
    用于显示单个环境参数
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
        font.setPointSize(12)
        font.setBold(True)
        self.title_label.setFont(font)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)
        
        # 数值标签
        self.value_label = QLabel("0.00")
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.value_label.setFont(font)
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.value_label)
        
        # 单位标签
        self.unit_label = QLabel(unit)
        font = QFont()
        font.setPointSize(10)
        self.unit_label.setFont(font)
        self.unit_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.unit_label)
        
    def update_value(self, value):
        """
        更新显示的数值
        
        Args:
            value: 新的数值
        """
        self.value_label.setText(f"{value:.2f}")


class MonitorWidget(QWidget):
    """
    环境监测主界面
    """
    def __init__(self):
        super().__init__()
        self.history_data = []
        self.init_ui()
        self.init_timer()
        
        # 加载历史数据
        self.load_history_data()
        
    def init_ui(self):
        """
        初始化界面
        """
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # 标题
        title_label = QLabel("秋月梨种植环境实时监测")
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 创建网格布局用于放置数据展示组件
        data_grid = QGridLayout()
        data_grid.setSpacing(10)
        
        # 创建四个数据展示组件
        self.temp_widget = DataDisplayWidget("温度", "°C")
        self.humidity_widget = DataDisplayWidget("湿度", "%")
        self.light_widget = DataDisplayWidget("光照", "lux")
        self.soil_widget = DataDisplayWidget("土壤湿度", "%")
        
        # 添加到网格布局
        data_grid.addWidget(self.temp_widget, 0, 0)
        data_grid.addWidget(self.humidity_widget, 0, 1)
        data_grid.addWidget(self.light_widget, 1, 0)
        data_grid.addWidget(self.soil_widget, 1, 1)
        
        layout.addLayout(data_grid)
        
        # 创建图表标签页
        self.chart_tabs = QTabWidget()
        
        # 创建折线图组件（用于查看历史变化）
        self.line_chart_widget = ChartWidget()
        self.chart_tabs.addTab(self.line_chart_widget, "历史变化趋势")
        
        # 创建柱状图组件（用于查看最新状态）
        self.bar_chart_widget = BarChartWidget()
        self.chart_tabs.addTab(self.bar_chart_widget, "当前状态")
        
        layout.addWidget(self.chart_tabs)
        
        # 设置初始大小比例
        layout.setStretch(0, 0)  # 标题
        layout.setStretch(1, 1)  # 数据网格
        layout.setStretch(2, 3)  # 图表标签页
        
        # 添加伸缩因子以填满窗口
        layout.addStretch(1)
        
    def init_timer(self):
        """
        初始化定时器
        """
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.load_history_data)
        self.refresh_timer.start(30000)  # 每30秒自动刷新一次历史数据
        
    def on_sensor_data_updated(self, env_data: EnvironmentData):
        """
        处理传感器数据更新
        
        Args:
            env_data: EnvironmentData对象
        """
        # 更新数值显示
        self.temp_widget.update_value(env_data.temperature)
        self.humidity_widget.update_value(env_data.humidity)
        self.light_widget.update_value(env_data.light)
        self.soil_widget.update_value(env_data.soil_moisture)
        
        # 更新折线图
        self.line_chart_widget.add_data_point(env_data)
        
        # 更新柱状图（显示最新状态）
        self.bar_chart_widget.update_data(env_data)
        
    def load_history_data(self):
        """
        加载历史数据
        """
        # 注意：这里需要主窗口传递历史数据
        pass
        
    def update_history_table(self, history_data):
        """
        更新历史数据表格
        
        Args:
            history_data: 历史数据列表
        """
        # 此方法在拆分后的页面中不再使用
        pass