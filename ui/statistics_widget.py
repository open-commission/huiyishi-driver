#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
统计分析界面
显示会议室使用和设备运行的统计数据
"""

import sys
import random
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QLabel, QFrame, QApplication, QPushButton)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QPainter, QPen, QBrush
from datetime import datetime, timedelta


class StatisticsChart(QWidget):
    """
    统计图表组件
    """
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.title = title
        self.data = []  # [(label, value), ...]
        self.setMinimumHeight(200)
        
    def set_data(self, data):
        """
        设置图表数据
        
        Args:
            data: [(label, value), ...] 格式的数据
        """
        self.data = data
        self.update()
        
    def paintEvent(self, event):
        """
        绘制事件处理
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 绘制背景
        painter.fillRect(self.rect(), Qt.GlobalColor.white)
        
        if not self.data:
            # 无数据提示
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "暂无数据")
            return
            
        # 绘制标题
        if self.title:
            title_font = QFont()
            title_font.setPointSize(12)
            title_font.setBold(True)
            painter.setFont(title_font)
            
            painter.drawText(self.rect().left(), self.rect().top(), 
                           self.rect().width(), 30,
                           Qt.AlignmentFlag.AlignCenter, self.title)
        
        # 计算绘图区域
        chart_rect = self.rect().adjusted(40, 40, -20, -20)
        
        # 查找最大值
        max_value = max([item[1] for item in self.data]) if self.data else 1
        max_value = max_value if max_value > 0 else 1  # 避免除零错误
        
        # 绘制柱状图
        bar_count = len(self.data)
        bar_width = chart_rect.width() / (bar_count * 2) if bar_count > 0 else 0
        spacing = bar_width
        
        for i, (label, value) in enumerate(self.data):
            # 计算柱子位置和高度
            x = chart_rect.left() + i * (bar_width + spacing) + spacing / 2
            bar_height = (value / max_value) * chart_rect.height()
            y = chart_rect.bottom() - bar_height
            
            # 绘制柱子
            painter.setBrush(QBrush(QColor(50, 150, 255)))
            painter.setPen(QPen(QColor(30, 100, 200)))
            painter.drawRect(int(x), int(y), int(bar_width), int(bar_height))
            
            # 绘制标签
            painter.setPen(QPen(Qt.GlobalColor.black))
            painter.drawText(int(x), chart_rect.bottom() + 15, int(bar_width), 20, 
                           Qt.AlignmentFlag.AlignCenter, str(label))
            
            # 绘制数值
            if bar_height > 10:  # 只有柱子足够高时才绘制数值
                painter.drawText(int(x), int(y - 15), int(bar_width), 20,
                               Qt.AlignmentFlag.AlignCenter, str(value))


class StatisticsWidget(QWidget):
    """
    统计分析界面
    """
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_sample_data()
        
    def init_ui(self):
        """
        初始化界面
        """
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # 标题
        title_label = QLabel("统计分析")
        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 会议室使用统计
        usage_group = QFrame()
        usage_group.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        usage_layout = QVBoxLayout(usage_group)
        
        usage_title = QLabel("会议室使用统计 (小时)")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        usage_title.setFont(font)
        usage_layout.addWidget(usage_title)
        
        self.usage_chart = StatisticsChart()
        usage_layout.addWidget(self.usage_chart)
        
        layout.addWidget(usage_group)
        
        # 设备运行统计
        device_group = QFrame()
        device_group.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        device_layout = QVBoxLayout(device_group)

        device_title = QLabel("设备运行统计 (小时)")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        device_title.setFont(font)
        device_layout.addWidget(device_title)
        
        self.device_chart = StatisticsChart()
        device_layout.addWidget(self.device_chart)
        
        layout.addWidget(device_group)
        
    def load_sample_data(self):
        """
        加载示例统计数据
        """
        # 会议室使用统计数据
        usage_data = [
            ("会议室A", 45),
            ("会议室B", 52),
            ("会议室C", 48),
            ("会议室D", 55),
            ("会议室E", 49),
            ("会议室F", 51)
        ]
        self.usage_chart.set_data(usage_data)
        
        # 设备运行统计
        device_data = [
            ("空调", 15),
            ("投影仪", 28),
            ("音响", 32),
            ("照明", 18)
        ]
        self.device_chart.set_data(device_data)


if __name__ == "__main__":
    # 测试代码
    app = QApplication(sys.argv)
    widget = StatisticsWidget()
    widget.show()
    sys.exit(app.exec())