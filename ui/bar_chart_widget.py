#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
柱状图显示组件
用于显示当前环境数据状态
"""

import sys
import numpy as np
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QPen, QColor, QFont, QBrush
from models.environment_model import EnvironmentData


class BarChartWidget(QWidget):
    """
    柱状图显示组件（用于显示当前状态）
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_data = None
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
        
    def update_data(self, env_data: EnvironmentData):
        """
        更新当前数据显示
        
        Args:
            env_data: EnvironmentData对象
        """
        self.current_data = env_data
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
        if not self.current_data:
            self.draw_no_data_message(painter)
            return
            
        # 绘制图表
        self.draw_grid(painter)
        self.draw_axes(painter)
        self.draw_bar_chart(painter)
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
        
        # 绘制水平网格线 (10条)
        pen = QPen(QColor(220, 220, 220))
        pen.setWidth(1)
        painter.setPen(pen)
        
        grid_lines = 10
        y_step = chart_rect.height() / grid_lines
        for i in range(grid_lines + 1):
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
        
        # Y轴标签 (0-100)
        grid_lines = 10
        y_step = chart_rect.height() / grid_lines
        value_step = 100 / grid_lines  # 假设最大值为100
        
        for i in range(grid_lines + 1):
            y = chart_rect.bottom() - i * y_step
            value = i * value_step
            
            # 绘制标签
            label = str(int(value))
            label_rect = QRectF(chart_rect.left() - 40, y - 10, 35, 20)
            painter.drawText(label_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, label)
            
        # 绘制X轴标签（数据类型）
        data_types = [
            ('temperature', '温度'),
            ('humidity', '湿度'),
            ('light', '光照'),
            ('soil_moisture', '土壤湿度')
        ]
        
        # 计算柱状图参数，确保柱子和标签对齐
        total_bars = len(data_types)
        spacing_count = total_bars + 1  # 两侧各一个间隔
        bar_count = total_bars
        
        # 计算间隔和柱子宽度
        total_width = chart_rect.width()
        spacing_width = total_width / (spacing_count + bar_count)  # 间隔宽度
        bar_width = spacing_width  # 柱子宽度等于间隔宽度
        
        for i, (key, label) in enumerate(data_types):
            # 计算柱子的中心位置
            x = chart_rect.left() + (i + 1) * spacing_width + i * bar_width + bar_width / 2
            label_rect = QRectF(x - 30, chart_rect.bottom() + 5, 60, 20)
            painter.drawText(label_rect, Qt.AlignmentFlag.AlignCenter, label)
                
        painter.restore()
        
    def draw_bar_chart(self, painter):
        """
        绘制柱状图
        
        Args:
            painter: QPainter对象
        """
        if not self.current_data:
            return
            
        painter.save()
        
        width = self.width()
        height = self.height()
        chart_rect = QRectF(self.margin, self.margin, 
                           width - 2 * self.margin, 
                           height - 2 * self.margin)
        
        # 数据类型
        data_types = [
            ('temperature', '温度', 40),      # 温度最大值40度
            ('humidity', '湿度', 100),       # 湿度最大值100%
            ('light', '光照', 100),          # 光照最大值100k lux (实际值除以1000)
            ('soil_moisture', '土壤湿度', 100) # 土壤湿度最大值100%
        ]
        
        # 计算柱状图参数，确保柱子和标签对齐
        total_bars = len(data_types)
        spacing_count = total_bars + 1  # 两侧各一个间隔
        bar_count = total_bars
        
        # 计算间隔和柱子宽度
        total_width = chart_rect.width()
        spacing_width = total_width / (spacing_count + bar_count)  # 间隔宽度
        bar_width = spacing_width  # 柱子宽度等于间隔宽度
        
        # 绘制每个数据的柱状图
        for i, (key, label, max_value) in enumerate(data_types):
            # 获取值
            if key == 'temperature':
                value = self.current_data.temperature
            elif key == 'humidity':
                value = self.current_data.humidity
            elif key == 'light':
                value = self.current_data.light / 1000  # 转换为k lux
            else:  # soil_moisture
                value = self.current_data.soil_moisture
            
            # 设置画笔和画刷
            color = self.colors[key]
            painter.setPen(QPen(color, 1))
            painter.setBrush(QBrush(color))
            
            # 计算柱状图高度
            bar_height = (value / max_value) * chart_rect.height()
            
            # 绘制柱状图
            x = chart_rect.left() + (i + 1) * spacing_width + i * bar_width
            y = chart_rect.bottom() - bar_height
            rect = QRectF(x, y, bar_width, bar_height)
            painter.drawRect(rect)
            
            # 绘制数值标签
            painter.setPen(Qt.GlobalColor.black)
            font = QFont()
            font.setPointSize(9)
            painter.setFont(font)
            value_text = f"{value:.1f}"
            text_rect = QRectF(x, y - 20, bar_width, 20)
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, value_text)
                
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
    
    widget = BarChartWidget()
    
    # 生成测试数据
    import random
    from datetime import datetime
    data = EnvironmentData(
        temperature=random.uniform(20, 35),
        humidity=random.uniform(40, 80),
        light=random.uniform(2000, 10000),
        soil_moisture=random.uniform(50, 90)
    )
    data.timestamp = datetime.now()
    widget.update_data(data)
    
    widget.show()
    sys.exit(app.exec())