#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
统计分析界面
显示种植过程中的各种统计数据
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
            painter.drawText(10, 20, self.title)
            
        # 计算绘图区域
        margin = 40
        chart_rect = self.rect().adjusted(margin, 30, -margin, -margin)
        
        if chart_rect.width() <= 0 or chart_rect.height() <= 0:
            return
            
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
        
        # 产量统计
        yield_group = QFrame()
        yield_group.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        yield_layout = QVBoxLayout(yield_group)
        
        yield_title = QLabel("产量统计 (公斤)")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        yield_title.setFont(font)
        yield_layout.addWidget(yield_title)
        
        self.yield_chart = StatisticsChart()
        yield_layout.addWidget(self.yield_chart)
        
        layout.addWidget(yield_group)
        
        # 质量等级统计
        quality_group = QFrame()
        quality_group.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        quality_layout = QVBoxLayout(quality_group)
        
        quality_title = QLabel("质量等级分布")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        quality_title.setFont(font)
        quality_layout.addWidget(quality_title)
        
        self.quality_chart = StatisticsChart()
        quality_layout.addWidget(self.quality_chart)
        
        layout.addWidget(quality_group)
        
        # 环境数据统计
        env_group = QFrame()
        env_group.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        env_layout = QVBoxLayout(env_group)
        
        env_title = QLabel("平均环境数据")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        env_title.setFont(font)
        env_layout.addWidget(env_title)
        
        # 环境数据网格
        env_grid = QGridLayout()
        env_grid.setSpacing(10)
        
        env_stats = [
            ("温度(°C)", "25.3"),
            ("湿度(%)", "62.5"),
            ("光照(k lux)", "15.2"),
            ("土壤湿度(%)", "68.7")
        ]
        
        for i, (label, value) in enumerate(env_stats):
            stat_label = QLabel(label)
            stat_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            stat_value = QLabel(value)
            stat_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
            font = QFont()
            font.setPointSize(16)
            font.setBold(True)
            stat_value.setFont(font)
            
            row = i // 2
            col = (i % 2) * 2
            env_grid.addWidget(stat_label, row, col)
            env_grid.addWidget(stat_value, row, col + 1)
            
        env_layout.addLayout(env_grid)
        layout.addWidget(env_group)
        
    def load_sample_data(self):
        """
        加载示例统计数据
        """
        # 产量统计数据
        yield_data = [
            ("树1", 45),
            ("树2", 52),
            ("树3", 48),
            ("树4", 55),
            ("树5", 49),
            ("树6", 51)
        ]
        self.yield_chart.set_data(yield_data)
        
        # 质量等级分布
        quality_data = [
            ("特级", 15),
            ("一级", 28),
            ("二级", 32),
            ("三级", 18)
        ]
        self.quality_chart.set_data(quality_data)


if __name__ == "__main__":
    # 测试代码
    app = QApplication(sys.argv)
    widget = StatisticsWidget()
    widget.show()
    sys.exit(app.exec())