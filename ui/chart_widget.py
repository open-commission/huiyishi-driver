#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
图表显示组件
用于可视化环境数据历史记录（折线图）
"""

import sys
import numpy as np
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QPen, QColor, QFont, QPolygonF, QBrush
from models.environment_model import EnvironmentData


class ChartWidget(QWidget):
    """
    折线图显示组件（用于查看历史变化）
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data_history = []
        self.max_data_points = 50  # 最大显示数据点数
        self.setMinimumHeight(300)
        
        # 图表颜色设置
        self.colors = {
            'temperature': QColor(255, 50, 50),      # 红色
            'humidity': QColor(50, 150, 255),        # 蓝色
            'light': QColor(255, 200, 50),           # 黄色
            'soil_moisture': QColor(50, 200, 50)     # 绿色
        }
        
        # 图表参数
        self.margin = 50
        self.grid_lines = 10
        
    def add_data_point(self, env_data: EnvironmentData):
        """
        添加数据点
        
        Args:
            env_data: EnvironmentData对象
        """
        self.data_history.append(env_data)
        
        # 保持数据点数量在限制范围内
        if len(self.data_history) > self.max_data_points:
            self.data_history.pop(0)
            
        self.update()
        
    def paintEvent(self, event):
        """
        绘制事件处理
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 绘制背景
        painter.fillRect(self.rect(), Qt.GlobalColor.white)
        
        # 如果没有数据，显示提示信息
        if not self.data_history:
            self.draw_no_data_message(painter)
            return
            
        # 绘制图表
        self.draw_grid(painter)
        self.draw_axes(painter)
        self.draw_line_chart(painter)
        self.draw_legend(painter)
        
    def draw_no_data_message(self, painter):
        """
        绘制无数据提示信息
        
        Args:
            painter: QPainter对象
        """
        painter.save()
        font = QFont()
        font.setPointSize(16)
        painter.setFont(font)
        painter.setPen(QColor(150, 150, 150))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "暂无数据")
        painter.restore()
        
    def draw_grid(self, painter):
        """
        绘制网格线
        
        Args:
            painter: QPainter对象
        """
        painter.save()
        
        # 计算绘图区域
        width = self.width()
        height = self.height()
        chart_rect = QRectF(self.margin, self.margin, 
                           width - 2 * self.margin, 
                           height - 2 * self.margin)
        
        # 绘制垂直网格线
        pen = QPen(QColor(220, 220, 220))
        pen.setWidth(1)
        painter.setPen(pen)
        
        x_step = chart_rect.width() / self.grid_lines
        for i in range(self.grid_lines + 1):
            x = chart_rect.left() + i * x_step
            painter.drawLine(int(x), int(chart_rect.top()), 
                           int(x), int(chart_rect.bottom()))
            
        # 绘制水平网格线
        y_step = chart_rect.height() / self.grid_lines
        for i in range(self.grid_lines + 1):
            y = chart_rect.bottom() - i * y_step
            painter.drawLine(int(chart_rect.left()), int(y), 
                           int(chart_rect.right()), int(y))
            
        painter.restore()
        
    def draw_axes(self, painter):
        """
        绘制坐标轴和标签
        
        Args:
            painter: QPainter对象
        """
        painter.save()
        
        width = self.width()
        height = self.height()
        chart_rect = QRectF(self.margin, self.margin, 
                           width - 2 * self.margin, 
                           height - 2 * self.margin)
        
        # 绘制坐标轴
        pen = QPen(Qt.GlobalColor.black)
        pen.setWidth(2)
        painter.setPen(pen)
        
        # X轴
        painter.drawLine(int(chart_rect.left()), int(chart_rect.bottom()), 
                        int(chart_rect.right()), int(chart_rect.bottom()))
        
        # Y轴
        painter.drawLine(int(chart_rect.left()), int(chart_rect.bottom()), 
                        int(chart_rect.left()), int(chart_rect.top()))
        
        # 绘制Y轴标签（数值）
        font = QFont()
        font.setPointSize(8)
        painter.setFont(font)
        painter.setPen(Qt.GlobalColor.black)
        
        # Y轴标签
        max_value = 100  # 假设最大值为100
        y_step = chart_rect.height() / self.grid_lines
        value_step = max_value / self.grid_lines
        
        for i in range(self.grid_lines + 1):
            y = chart_rect.bottom() - i * y_step
            value = i * value_step
            
            # 绘制标签
            label = str(int(value))
            label_rect = QRectF(chart_rect.left() - 40, y - 10, 35, 20)
            painter.drawText(label_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, label)
            
        # 绘制X轴标签（时间点）
        if self.data_history:
            x_step = chart_rect.width() / (len(self.data_history) - 1) if len(self.data_history) > 1 else 0
            
            # 只显示部分时间点以避免标签重叠
            show_count = min(10, len(self.data_history))
            step = max(1, len(self.data_history) // show_count)
            
            for i in range(0, len(self.data_history), step):
                x = chart_rect.left() + i * x_step
                data_point = self.data_history[i]
                
                # 简化时间显示
                time_label = data_point.timestamp.strftime("%H:%M")
                label_rect = QRectF(x - 20, chart_rect.bottom() + 5, 40, 20)
                painter.drawText(label_rect, Qt.AlignmentFlag.AlignCenter, time_label)
                
        painter.restore()
        
    def draw_line_chart(self, painter):
        """
        绘制折线图
        
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
        
        # 绘制每种数据的线条
        data_types = ['temperature', 'humidity', 'light', 'soil_moisture']
        max_values = [40, 100, 100000, 100]  # 每种数据的最大值
        
        for idx, data_type in enumerate(data_types):
            pen = QPen(self.colors[data_type])
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
                    # 光照数据需要特殊处理，因为范围很大
                    value = data_point.light / 1000  # 转换为k lux
                else:  # soil_moisture
                    value = data_point.soil_moisture
                
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
        绘制图例
        
        Args:
            painter: QPainter对象
        """
        painter.save()
        
        # 图例位置
        legend_x = self.width() - 150
        legend_y = self.margin + 20
        legend_width = 130
        legend_height = 80
        
        # 绘制图例背景
        painter.setBrush(QColor(255, 255, 255, 200))  # 半透明白色
        painter.setPen(QColor(180, 180, 180))
        painter.drawRect(legend_x, legend_y, legend_width, legend_height)
        
        # 绘制图例项
        data_types = [
            ('temperature', '温度'),
            ('humidity', '湿度'),
            ('light', '光照'),
            ('soil_moisture', '土壤湿度')
        ]
        
        font = QFont()
        font.setPointSize(9)
        painter.setFont(font)
        
        for i, (data_type, label) in enumerate(data_types):
            y_pos = legend_y + 10 + i * 18
            
            # 绘制颜色标识
            painter.setPen(QPen(self.colors[data_type], 2))
            painter.drawLine(legend_x + 10, y_pos + 5, legend_x + 30, y_pos + 5)
            
            # 绘制标签
            painter.setPen(Qt.GlobalColor.black)
            painter.drawText(legend_x + 35, y_pos, 80, 20, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, label)
            
        painter.restore()


if __name__ == "__main__":
    # 测试代码
    app = QApplication(sys.argv)
    
    widget = ChartWidget()
    
    # 生成测试数据
    import random
    from datetime import datetime, timedelta
    for i in range(30):
        data = EnvironmentData(
            temperature=random.uniform(20, 35),
            humidity=random.uniform(40, 80),
            light=random.uniform(2000, 10000),
            soil_moisture=random.uniform(50, 90)
        )
        data.timestamp = datetime.now() - timedelta(minutes=(30-i)*5)
        widget.add_data_point(data)
    
    widget.show()
    sys.exit(app.exec())