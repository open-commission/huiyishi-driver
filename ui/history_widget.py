#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
会议室环境历史数据界面组件
显示会议室环境监测的历史数据
"""

import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QLabel, QFrame, QApplication, QPushButton, QTableWidget,
                             QTableWidgetItem, QHeaderView, QGroupBox, QSizePolicy)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor
from models.environment_model import EnvironmentData


class HistoryWidget(QWidget):
    """
    历史数据主界面，上下两个部分：上面现场从机，下面会议室从机
    """
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.history_data = []
        self.init_ui()
        
    def init_ui(self):
        """
        初始化界面
        """
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # 标题
        title_label = QLabel("环境监测历史数据 - 现场从机与会议室从机对比")
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 创建上下两个历史数据区域
        history_layout = QVBoxLayout()
        history_layout.setSpacing(10)
        
        # 上半部分：现场从机历史数据
        field_group = QGroupBox("现场从机历史数据")
        field_layout = QVBoxLayout(field_group)
        
        self.field_table = QTableWidget()
        self.field_table.setColumnCount(6)
        self.field_table.setHorizontalHeaderLabels(["时间", "温度(°C)", "湿度(%)", "光照(lux)", "二氧化碳(ppm)", "PM2.5(μg/m³)"])
        
        # 设置表格属性 - 不显示滚动条
        self.field_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.field_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.field_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.field_table.verticalHeader().setVisible(False)
        self.field_table.setAlternatingRowColors(True)
        self.field_table.setMaximumHeight(200)  # 限制高度，只显示几行
        
        field_layout.addWidget(self.field_table)
        history_layout.addWidget(field_group)
        
        # 下半部分：会议室从机历史数据
        meeting_group = QGroupBox("会议室从机历史数据")
        meeting_layout = QVBoxLayout(meeting_group)
        
        self.meeting_table = QTableWidget()
        self.meeting_table.setColumnCount(4)
        self.meeting_table.setHorizontalHeaderLabels(["时间", "温度(°C)", "湿度(%)", "光照(lux)"])
        
        # 设置表格属性 - 不显示滚动条
        self.meeting_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.meeting_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.meeting_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.meeting_table.verticalHeader().setVisible(False)
        self.meeting_table.setAlternatingRowColors(True)
        self.meeting_table.setMaximumHeight(200)  # 限制高度，只显示几行
        
        meeting_layout.addWidget(self.meeting_table)
        history_layout.addWidget(meeting_group)
        
        layout.addLayout(history_layout)
        
        # 设置布局权重，让两个表格各占一半空间
        history_layout.setStretch(0, 1)  # 现场从机表格
        history_layout.setStretch(1, 1)  # 会议室从机表格
        
    def update_history_table(self, history_data):
        """
        更新历史数据表格（为两个表格提供数据）
        
        Args:
            history_data: 历史数据列表
        """
        # 只显示最新的数据（根据表格高度自动调整显示行数）
        max_rows = 5  # 最多显示5行
        display_data = history_data[-max_rows:] if len(history_data) > max_rows else history_data
        
        # 更新现场从机历史数据表格
        self.field_table.setRowCount(0)
        self.field_table.setRowCount(len(display_data))
        
        for row, data in enumerate(display_data):
            # 时间
            time_item = QTableWidgetItem(data.timestamp.strftime("%Y-%m-%d %H:%M:%S"))
            self.field_table.setItem(row, 0, time_item)
            
            # 温度
            temp_item = QTableWidgetItem(f"{data.temperature:.2f}")
            self.field_table.setItem(row, 1, temp_item)
            
            # 湿度
            humidity_item = QTableWidgetItem(f"{data.humidity:.2f}")
            self.field_table.setItem(row, 2, humidity_item)
            
            # 光照
            light_item = QTableWidgetItem(f"{data.light:.2f}")
            self.field_table.setItem(row, 3, light_item)
            
            # 二氧化碳
            co2_item = QTableWidgetItem(f"{data.co2:.2f}")
            self.field_table.setItem(row, 4, co2_item)
            
            # PM2.5
            pm25_item = QTableWidgetItem(f"{data.pm25:.2f}")
            self.field_table.setItem(row, 5, pm25_item)
        
        # 更新会议室从机历史数据表格
        self.meeting_table.setRowCount(0)
        self.meeting_table.setRowCount(len(display_data))
        
        for row, data in enumerate(display_data):
            # 时间
            time_item = QTableWidgetItem(data.timestamp.strftime("%Y-%m-%d %H:%M:%S"))
            self.meeting_table.setItem(row, 0, time_item)
            
            # 温度
            temp_item = QTableWidgetItem(f"{data.temperature:.2f}")
            self.meeting_table.setItem(row, 1, temp_item)
            
            # 湿度
            humidity_item = QTableWidgetItem(f"{data.humidity:.2f}")
            self.meeting_table.setItem(row, 2, humidity_item)
            
            # 光照
            light_item = QTableWidgetItem(f"{data.light:.2f}")
            self.meeting_table.setItem(row, 3, light_item)

