#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
历史数据界面组件
显示环境监测的历史数据
"""

import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QLabel, QFrame, QApplication, QPushButton, QTableWidget,
                             QTableWidgetItem, QHeaderView, QGroupBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor
from models.environment_model import EnvironmentData


class HistoryWidget(QWidget):
    """
    历史数据主界面
    """
    def __init__(self):
        super().__init__()
        self.history_data = []
        self.init_ui()
        
    def init_ui(self):
        """
        初始化界面
        """
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # 标题
        title_label = QLabel("环境监测历史数据")
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 创建历史数据按钮
        button_layout = QHBoxLayout()
        self.refresh_button = QPushButton("刷新历史数据")
        self.refresh_button.clicked.connect(self.load_history_data)
        button_layout.addWidget(self.refresh_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # 创建历史数据表格
        history_group = QGroupBox("历史数据记录")
        history_layout = QVBoxLayout(history_group)
        
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["时间", "温度(°C)", "湿度(%)", "光照(lux)", "土壤湿度(%)"])
        
        # 设置表格属性
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.setAlternatingRowColors(True)
        self.history_table.setMinimumHeight(300)
        
        history_layout.addWidget(self.history_table)
        layout.addWidget(history_group)
        
        # 添加伸缩因子以填满窗口
        layout.addStretch(1)
        
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
        # 清空表格
        self.history_table.setRowCount(0)
        
        # 添加历史数据到表格
        self.history_table.setRowCount(len(history_data))
        
        for row, data in enumerate(history_data):
            # 时间
            time_item = QTableWidgetItem(data.timestamp.strftime("%Y-%m-%d %H:%M:%S"))
            self.history_table.setItem(row, 0, time_item)
            
            # 温度
            temp_item = QTableWidgetItem(f"{data.temperature:.2f}")
            self.history_table.setItem(row, 1, temp_item)
            
            # 湿度
            humidity_item = QTableWidgetItem(f"{data.humidity:.2f}")
            self.history_table.setItem(row, 2, humidity_item)
            
            # 光照
            light_item = QTableWidgetItem(f"{data.light:.2f}")
            self.history_table.setItem(row, 3, light_item)
            
            # 土壤湿度
            soil_item = QTableWidgetItem(f"{data.soil_moisture:.2f}")
            self.history_table.setItem(row, 4, soil_item)
            
        # 如果有数据，滚动到最后一行
        if history_data:
            self.history_table.scrollToBottom()