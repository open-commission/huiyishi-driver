#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
种植记录界面
用于记录每日种植效果和异常情况
"""

import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QFrame, QApplication, QPushButton, QTextEdit,
                             QCalendarWidget, QListWidget, QListWidgetItem)
from PyQt6.QtCore import Qt, QDate, QTimer
from PyQt6.QtGui import QFont, QColor


class PlantingRecordWidget(QWidget):
    """
    种植记录界面
    """
    def __init__(self):
        super().__init__()
        self.records = {}  # 存储每日记录
        self.current_date = QDate.currentDate()
        self.init_ui()
        self.load_sample_records()
        
    def init_ui(self):
        """
        初始化界面
        """
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # 标题
        title_label = QLabel("种植记录")
        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 日历组件
        self.calendar = QCalendarWidget()
        self.calendar.setSelectedDate(self.current_date)
        self.calendar.clicked.connect(self.on_date_selected)
        layout.addWidget(self.calendar)
        
        # 日期显示
        self.date_label = QLabel(self.current_date.toString("yyyy年MM月dd日"))
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.date_label.setFont(font)
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.date_label)
        
        # 记录编辑区域
        record_group = QFrame()
        record_group.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        record_layout = QVBoxLayout(record_group)
        
        record_title = QLabel("当日记录")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        record_title.setFont(font)
        record_layout.addWidget(record_title)
        
        # 记录文本框
        self.record_text = QTextEdit()
        self.record_text.setPlaceholderText("请输入当日种植效果记录...")
        self.record_text.setMaximumHeight(100)
        record_layout.addWidget(self.record_text)
        
        # 异常情况选择
        anomaly_layout = QHBoxLayout()
        anomaly_layout.addWidget(QLabel("异常情况:"))
        
        self.anomaly_buttons = []
        anomalies = ["无异常", "虫灾", "水灾", "温度过高", "温度过低", "干旱", "病害"]
        self.selected_anomaly = "无异常"
        
        for anomaly in anomalies:
            button = QPushButton(anomaly)
            button.setCheckable(True)
            if anomaly == "无异常":
                button.setChecked(True)
            button.clicked.connect(lambda checked, a=anomaly: self.select_anomaly(a))
            anomaly_layout.addWidget(button)
            self.anomaly_buttons.append(button)
            
        record_layout.addLayout(anomaly_layout)
        
        # 保存按钮
        self.save_button = QPushButton("保存记录")
        self.save_button.clicked.connect(self.save_record)
        record_layout.addWidget(self.save_button)
        
        layout.addWidget(record_group)
        
        # 历史记录区域
        history_group = QFrame()
        history_group.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        history_layout = QVBoxLayout(history_group)
        
        history_title = QLabel("历史记录")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        history_title.setFont(font)
        history_layout.addWidget(history_title)
        
        self.history_list = QListWidget()
        history_layout.addWidget(self.history_list)
        
        layout.addWidget(history_group)
        
        # 添加伸缩因子以填满窗口
        layout.addStretch(1)
        
        # 创建定时器用于按钮文本恢复
        self.button_timer = QTimer()
        self.button_timer.setSingleShot(True)
        self.button_timer.timeout.connect(self.reset_save_button_text)
        
    def on_date_selected(self, date):
        """
        处理日期选择事件
        
        Args:
            date: 选中的日期
        """
        self.current_date = date
        self.date_label.setText(date.toString("yyyy年MM月dd日"))
        
        # 加载选中日期的记录
        date_key = date.toString("yyyy-MM-dd")
        if date_key in self.records:
            record_data = self.records[date_key]
            self.record_text.setPlainText(record_data["record"])
            self.select_anomaly(record_data["anomaly"])
        else:
            self.record_text.clear()
            self.select_anomaly("无异常")
            
    def select_anomaly(self, anomaly):
        """
        选择异常情况
        
        Args:
            anomaly: 异常情况
        """
        self.selected_anomaly = anomaly
        # 更新按钮状态
        for button in self.anomaly_buttons:
            if button.text() == anomaly:
                button.setChecked(True)
            else:
                button.setChecked(False)
                
    def save_record(self):
        """
        保存记录
        """
        date_key = self.current_date.toString("yyyy-MM-dd")
        record_data = {
            "date": self.current_date.toString("yyyy年MM月dd日"),
            "record": self.record_text.toPlainText(),
            "anomaly": self.selected_anomaly
        }
        self.records[date_key] = record_data
        
        # 更新历史记录显示
        self.update_history_display()
        
        # 显示保存成功提示
        self.save_button.setText("保存成功")
        self.button_timer.start(1000)  # 1秒后恢复按钮文本
        
    def reset_save_button_text(self):
        """
        恢复保存按钮的文本
        """
        self.save_button.setText("保存记录")
        
    def update_history_display(self):
        """
        更新历史记录显示
        """
        self.history_list.clear()
        # 按日期倒序显示
        for date_key in sorted(self.records.keys(), reverse=True):
            record_data = self.records[date_key]
            item_text = f"{record_data['date']} - {record_data['anomaly']}"
            if record_data['record']:
                item_text += f"\n{record_data['record'][:30]}..." if len(record_data['record']) > 30 else f"\n{record_data['record']}"
                
            item = QListWidgetItem(item_text)
            if record_data['anomaly'] != "无异常":
                item.setForeground(QColor("red"))
            self.history_list.addItem(item)
            
    def load_sample_records(self):
        """
        加载示例记录数据
        """
        # 添加一些示例记录
        today = QDate.currentDate()
        yesterday = today.addDays(-1)
        last_week = today.addDays(-7)
        
        self.records = {
            today.toString("yyyy-MM-dd"): {
                "date": today.toString("yyyy年MM月dd日"),
                "record": "今日进行浇水和施肥，植株生长状态良好。",
                "anomaly": "无异常"
            },
            yesterday.toString("yyyy-MM-dd"): {
                "date": yesterday.toString("yyyy年MM月dd日"),
                "record": "发现少量虫害，已进行局部杀虫处理。",
                "anomaly": "虫灾"
            },
            last_week.toString("yyyy-MM-dd"): {
                "date": last_week.toString("yyyy年MM月dd日"),
                "record": "连续高温，增加浇水频率。",
                "anomaly": "温度过高"
            }
        }
        
        self.update_history_display()


if __name__ == "__main__":
    # 测试代码
    app = QApplication(sys.argv)
    widget = PlantingRecordWidget()
    widget.show()
    sys.exit(app.exec())