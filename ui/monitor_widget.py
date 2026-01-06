#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
会议室环境监测界面组件
显示实时会议室环境数据和可视化图表
"""

import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QLabel, QFrame, QApplication, QPushButton, QTableWidget,
                             QTableWidgetItem, QHeaderView, QGroupBox, QTabWidget, QSizePolicy)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor, QPen, QPainter, QBrush
from PyQt6.QtCore import QRectF  # QRectF 位于 QtCore 模块中
from ui.chart_widget import ChartWidget
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


class FieldChartWidget(ChartWidget):
    """
    现场从机折线图组件
    显示温度、湿度、光照、二氧化碳、PM2.5
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        # 重新定义颜色以适应现场从机的参数
        self.colors = {
            'temperature': QColor(255, 50, 50),      # 红色 - 温度
            'humidity': QColor(50, 150, 255),        # 蓝色 - 湿度
            'light': QColor(255, 200, 50),           # 黄色 - 光照
            'co2': QColor(50, 200, 50),              # 绿色 - 二氧化碳
            'pm25': QColor(150, 50, 200)             # 紫色 - PM2.5
        }
        
    def draw_data_lines(self, painter):
        """
        绘制现场从机数据线
        
        Args:
            painter: QPainter对象
        """
        if len(self.data_history) < 2:
            return
            
        painter.save()
        
        width = self.width()
        height = self.height()
        chart_rect = QRectF(self.margin, self.margin, 
                           width - 2 * self.margin, 
                           height - 2 * self.margin)
        
        # 数据范围
        x_step = chart_rect.width() / (len(self.data_history) - 1) if len(self.data_history) > 1 else 0
        
        # 绘制现场从机数据的线条：温度、湿度、光照、二氧化碳、PM2.5
        data_types = ['temperature', 'humidity', 'light', 'co2', 'pm25']
        # 最大值范围
        max_values = [40, 100, 100, 2000, 500]  # [温度, 湿度, 光照(klux), 二氧化碳, PM2.5]
        
        for idx, data_type in enumerate(data_types):
            pen = QPen(list(self.colors.values())[idx])
            pen.setWidth(2)
            painter.setPen(pen)
            
            points = []
            max_value = max_values[idx]
            
            for i, data_point in enumerate(self.data_history):
                x = chart_rect.left() + i * x_step
                
                # 根据数据类型获取值
                if data_type == 'temperature':
                    value = data_point.temperature
                elif data_type == 'humidity':
                    value = data_point.humidity
                elif data_type == 'light':
                    # 光照数据需要特殊处理，转换为k lux
                    value = data_point.light / 1000
                elif data_type == 'co2':
                    value = data_point.co2
                else:  # pm25
                    value = data_point.pm25
                
                # 计算Y坐标（注意坐标系Y轴向下为正）
                y = chart_rect.bottom() - (value / max_value) * chart_rect.height()
                points.append((x, y))
                
            # 绘制折线
            for i in range(len(points) - 1):
                p1 = points[i]
                p2 = points[i + 1]
                painter.drawLine(int(p1[0]), int(p1[1]), int(p2[0]), int(p2[1]))
                
        painter.restore()
        
    def draw_legend(self, painter):
        """
        绘制现场从机图例
        
        Args:
            painter: QPainter对象
        """
        if not self.data_history:
            return
            
        painter.save()
        
        legend_x = self.width() - 150
        legend_y = self.margin

        # 绘制图例背景
        painter.setBrush(QColor(255, 255, 255, 200))  # 半透明白色
        painter.setPen(QColor(180, 180, 180))
        painter.drawRect(legend_x, legend_y, 130, 100)
        
        # 现场从机数据类型和标签
        data_types = [
            ('temperature', '温度'),
            ('humidity', '湿度'),
            ('light', '光照'),
            ('co2', '二氧化碳'),
            ('pm25', 'PM2.5')
        ]
        
        font = QFont()
        font.setPointSize(9)
        painter.setFont(font)
        
        for i, (data_type, label) in enumerate(data_types):
            y_pos = legend_y + 10 + i * 18
            
            # 绘制颜色标识
            color = self.colors[data_type]
            painter.setPen(QPen(color, 2))
            painter.drawLine(legend_x + 10, y_pos + 5, legend_x + 30, y_pos + 5)
            
            # 绘制标签
            painter.setPen(Qt.GlobalColor.black)
            painter.drawText(legend_x + 35, y_pos, 80, 20, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, label)
            
        painter.restore()


class MeetingChartWidget(ChartWidget):
    """
    会议室从机折线图组件
    显示温度、湿度、光照
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        # 重新定义颜色以适应会议室从机的参数
        self.colors = {
            'temperature': QColor(255, 50, 50),      # 红色 - 温度
            'humidity': QColor(50, 150, 255),        # 蓝色 - 湿度
            'light': QColor(255, 200, 50)            # 黄色 - 光照
        }
        
    def draw_data_lines(self, painter):
        """
        绘制会议室从机数据线
        
        Args:
            painter: QPainter对象
        """
        if len(self.data_history) < 2:
            return
            
        painter.save()
        
        width = self.width()
        height = self.height()
        chart_rect = QRectF(self.margin, self.margin, 
                           width - 2 * self.margin, 
                           height - 2 * self.margin)
        
        # 数据范围
        x_step = chart_rect.width() / (len(self.data_history) - 1) if len(self.data_history) > 1 else 0
        
        # 绘制会议室从机数据的线条：温度、湿度、光照
        data_types = ['temperature', 'humidity', 'light']
        # 最大值范围
        max_values = [40, 100, 100]  # [温度, 湿度, 光照(klux)]
        
        for idx, data_type in enumerate(data_types):
            pen = QPen(list(self.colors.values())[idx])
            pen.setWidth(2)
            painter.setPen(pen)
            
            points = []
            max_value = max_values[idx]
            
            for i, data_point in enumerate(self.data_history):
                x = chart_rect.left() + i * x_step
                
                # 根据数据类型获取值
                if data_type == 'temperature':
                    value = data_point.temperature
                elif data_type == 'humidity':
                    value = data_point.humidity
                else:  # light
                    # 光照数据需要特殊处理，转换为k lux
                    value = data_point.light / 1000
                
                # 计算Y坐标（注意坐标系Y轴向下为正）
                y = chart_rect.bottom() - (value / max_value) * chart_rect.height()
                points.append((x, y))
                
            # 绘制折线
            for i in range(len(points) - 1):
                p1 = points[i]
                p2 = points[i + 1]
                painter.drawLine(int(p1[0]), int(p1[1]), int(p2[0]), int(p2[1]))
                
        painter.restore()
        
    def draw_legend(self, painter):
        """
        绘制会议室从机图例
        
        Args:
            painter: QPainter对象
        """
        if not self.data_history:
            return
            
        painter.save()
        
        legend_x = self.width() - 150
        legend_y = self.margin

        # 绘制图例背景
        painter.setBrush(QColor(255, 255, 255, 200))  # 半透明白色
        painter.setPen(QColor(180, 180, 180))
        painter.drawRect(legend_x, legend_y, 130, 60)
        
        # 会议室从机数据类型和标签
        data_types = [
            ('temperature', '温度'),
            ('humidity', '湿度'),
            ('light', '光照')
        ]
        
        font = QFont()
        font.setPointSize(9)
        painter.setFont(font)
        
        for i, (data_type, label) in enumerate(data_types):
            y_pos = legend_y + 10 + i * 18
            
            # 绘制颜色标识
            color = self.colors[data_type]
            painter.setPen(QPen(color, 2))
            painter.drawLine(legend_x + 10, y_pos + 5, legend_x + 30, y_pos + 5)
            
            # 绘制标签
            painter.setPen(Qt.GlobalColor.black)
            painter.drawText(legend_x + 35, y_pos, 80, 20, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, label)
            
        painter.restore()


class MonitorWidget(QWidget):
    """
    会议室环境监测主界面
    """
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
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
        title_label = QLabel("环境监测 - 现场从机与会议室从机对比")
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 创建上下两个图表区域
        charts_layout = QVBoxLayout()
        charts_layout.setSpacing(10)
        
        # 上半部分：现场从机折线图
        field_group = QGroupBox("现场从机")
        field_layout = QVBoxLayout(field_group)
        
        # 现场从机折线图 - 显示温度、湿度、光照、二氧化碳、PM2.5
        self.field_chart_widget = FieldChartWidget()
        field_layout.addWidget(self.field_chart_widget)
        
        charts_layout.addWidget(field_group)
        
        # 下半部分：会议室从机折线图
        meeting_group = QGroupBox("会议室从机")
        meeting_layout = QVBoxLayout(meeting_group)
        
        # 会议室从机折线图 - 显示温度、湿度、光照
        self.meeting_chart_widget = MeetingChartWidget()
        meeting_layout.addWidget(self.meeting_chart_widget)
        
        charts_layout.addWidget(meeting_group)
        
        layout.addLayout(charts_layout)
        
        # 设置图表区域的比例
        charts_layout.setStretch(0, 1)  # 现场从机图表
        charts_layout.setStretch(1, 1)  # 会议室从机图表
        
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
        # 同时更新两个图表的数据
        self.field_chart_widget.add_data_point(env_data)
        self.meeting_chart_widget.add_data_point(env_data)
        
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
