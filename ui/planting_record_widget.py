#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
会议室记录界面
用于记录每日会议室使用情况和状态
"""

import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QFrame, QApplication, QPushButton,
                             QCalendarWidget, QListWidget, QListWidgetItem, QSizePolicy)
from PyQt6.QtCore import Qt, QDate, QTimer
from PyQt6.QtGui import QFont, QColor


class PlantingRecordWidget(QWidget):
    """
    会议室记录界面
    """
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
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
        title_label = QLabel("会议室使用记录")
        font = QFont()
        font.setPointSize(18)
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
        font.setPointSize(14)
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
        font.setPointSize(12)
        font.setBold(True)
        record_title.setFont(font)
        record_layout.addWidget(record_title)
        
        # 预定义状态按钮
        status_layout = QGridLayout()
        statuses = [
            "会议室空闲", "会议进行中", "设备维护", "清洁中", 
            "预约中", "已预订", "会议结束", "设备故障"
        ]
        
        self.status_buttons = []
        for i, status in enumerate(statuses):
            button = QPushButton(status)
            button.setCheckable(True)
            button.clicked.connect(lambda checked, s=status: self.select_status(s))
            status_layout.addWidget(button, i // 4, i % 4)
            self.status_buttons.append(button)
        
        record_layout.addLayout(status_layout)
        
        # 异常情况选择
        anomaly_title = QLabel("异常情况:")
        anomaly_title.setFont(QFont("", 12, QFont.Weight.Bold))
        record_layout.addWidget(anomaly_title)
        
        anomaly_layout = QGridLayout()
        anomalies = [
            "无异常", "设备故障", "空调异常", "照明异常", 
            "网络故障", "清洁问题", "预约冲突", "设备缺失",
            "温度异常", "湿度异常", "噪音干扰", "其他问题"
        ]
        
        self.anomaly_buttons = []
        self.selected_anomalies = set()
        
        for i, anomaly in enumerate(anomalies):
            button = QPushButton(anomaly)
            button.setCheckable(True)
            if anomaly == "无异常":
                button.setChecked(True)
            button.clicked.connect(lambda checked, a=anomaly: self.toggle_anomaly(a))
            anomaly_layout.addWidget(button, i // 4, i % 4)
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
        font.setPointSize(12)
        font.setBold(True)
        history_title.setFont(font)
        history_layout.addWidget(history_title)
        
        self.history_list = QListWidget()
        history_layout.addWidget(self.history_list)
        
        layout.addWidget(history_group)
        
        # 设置布局权重
        layout.setStretch(0, 0)  # 标题
        layout.setStretch(1, 0)  # 日历
        layout.setStretch(2, 0)  # 日期
        layout.setStretch(3, 1)  # 记录区域
        layout.setStretch(4, 1)  # 历史记录区域
        
    def on_date_selected(self, date):
        """
        处理日期选择事件
        
        Args:
            date: 选中的日期
        """
        self.current_date = date
        self.date_label.setText(date.toString("yyyy年MM月dd日"))
        
        # 重置所有按钮状态
        for button in self.status_buttons:
            button.setChecked(False)
        for button in self.anomaly_buttons:
            button.setChecked(False)
            
        # 加载选中日期的记录
        date_key = date.toString("yyyy-MM-dd")
        if date_key in self.records:
            record_data = self.records[date_key]
            # 恢复状态选择
            if "status" in record_data:
                for button in self.status_buttons:
                    if button.text() == record_data["status"]:
                        button.setChecked(True)
            # 恢复异常情况选择
            if "anomalies" in record_data:
                self.selected_anomalies = set(record_data["anomalies"])
                for button in self.anomaly_buttons:
                    if button.text() in self.selected_anomalies:
                        button.setChecked(True)
        else:
            # 默认选择"无异常"
            for button in self.anomaly_buttons:
                if button.text() == "无异常":
                    button.setChecked(True)
                    break
            
    def select_status(self, status):
        """
        选择会议室状态
        
        Args:
            status: 会议室状态
        """
        # 取消其他状态按钮的选中状态
        for button in self.status_buttons:
            if button.text() != status:
                button.setChecked(False)
                
    def toggle_anomaly(self, anomaly):
        """
        切换异常情况选择
        
        Args:
            anomaly: 异常情况
        """
        button = None
        for btn in self.anomaly_buttons:
            if btn.text() == anomaly:
                button = btn
                break
                
        if anomaly == "无异常":
            # 如果选择了"无异常"，则取消其他所有异常选择
            if button.isChecked():
                self.selected_anomalies.clear()
                for btn in self.anomaly_buttons:
                    if btn.text() != "无异常":
                        btn.setChecked(False)
                self.selected_anomalies.add("无异常")
            else:
                # 如果取消"无异常"选择，确保至少有一个其他异常被选中或清除所有选择
                button.setChecked(True)
        else:
            # 处理其他异常情况
            if button.isChecked():
                self.selected_anomalies.discard("无异常")
                for btn in self.anomaly_buttons:
                    if btn.text() == "无异常":
                        btn.setChecked(False)
                        break
                self.selected_anomalies.add(anomaly)
            else:
                self.selected_anomalies.discard(anomaly)
                # 如果没有选择任何异常，默认选择"无异常"
                if not self.selected_anomalies:
                    for btn in self.anomaly_buttons:
                        if btn.text() == "无异常":
                            btn.setChecked(True)
                            self.selected_anomalies.add("无异常")
                            break
                
    def save_record(self):
        """
        保存记录
        """
        date_key = self.current_date.toString("yyyy-MM-dd")
        
        # 获取选中的状态
        selected_status = None
        for button in self.status_buttons:
            if button.isChecked():
                selected_status = button.text()
                break
                
        # 构建记录数据
        record_data = {
            "date": self.current_date.toString("yyyy年MM月dd日"),
            "status": selected_status,
            "anomalies": list(self.selected_anomalies)
        }
        self.records[date_key] = record_data
        
        # 更新历史记录显示
        self.update_history_display()
        
        # 显示保存成功提示
        self.save_button.setText("保存成功")
        self.button_timer = QTimer()
        self.button_timer.setSingleShot(True)
        self.button_timer.timeout.connect(lambda: self.save_button.setText("保存记录"))
        self.button_timer.start(1000)
        
    def update_history_display(self):
        """
        更新历史记录显示
        """
        self.history_list.clear()
        # 按日期倒序显示
        for date_key in sorted(self.records.keys(), reverse=True):
            record_data = self.records[date_key]
            status_text = record_data.get("status", "未记录")
            anomalies_text = ", ".join(record_data.get("anomalies", ["无异常"]))
            
            item_text = f"{record_data['date']}\n状态: {status_text} | 异常: {anomalies_text}"
                
            item = QListWidgetItem(item_text)
            if "无异常" not in record_data.get("anomalies", []) or record_data.get("anomalies") != ["无异常"]:
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
                "status": "会议进行中",
                "anomalies": ["无异常"]
            },
            yesterday.toString("yyyy-MM-dd"): {
                "date": yesterday.toString("yyyy年MM月dd日"),
                "status": "设备维护",
                "anomalies": ["设备故障"]
            },
            last_week.toString("yyyy-MM-dd"): {
                "date": last_week.toString("yyyy年MM月dd日"),
                "status": "会议室空闲",
                "anomalies": ["温度异常"]
            }
        }
        
        self.update_history_display()


if __name__ == "__main__":
    # 测试代码
    app = QApplication(sys.argv)
    widget = PlantingRecordWidget()
    widget.show()
    sys.exit(app.exec())