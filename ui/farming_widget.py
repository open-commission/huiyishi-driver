#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
农事操作指导界面
提供种植过程中的农事操作建议
"""

import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QLabel, QFrame, QApplication, QPushButton, QTextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor


class FarmingTaskWidget(QFrame):
    """
    农事任务小部件
    """
    def __init__(self, title="", description="", parent=None):
        super().__init__(parent)
        self.title = title
        self.description = description
        
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setLineWidth(1)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        
        # 任务标题
        self.title_label = QLabel(title)
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.title_label.setFont(font)
        layout.addWidget(self.title_label)
        
        # 任务描述
        self.desc_label = QLabel(description)
        self.desc_label.setWordWrap(True)
        layout.addWidget(self.desc_label)
        
        # 状态按钮
        self.status_button = QPushButton("待执行")
        self.status_button.setFixedWidth(80)
        self.status_button.clicked.connect(self.toggle_status)
        layout.addWidget(self.status_button)
        
    def toggle_status(self):
        """
        切换任务状态
        """
        if self.status_button.text() == "待执行":
            self.status_button.setText("已完成")
            self.status_button.setStyleSheet("background-color: green; color: white;")
        else:
            self.status_button.setText("待执行")
            self.status_button.setStyleSheet("")
            
    def update_task(self, title, description):
        """
        更新任务信息
        
        Args:
            title: 任务标题
            description: 任务描述
        """
        self.title_label.setText(title)
        self.desc_label.setText(description)


class FarmingWidget(QWidget):
    """
    农事操作指导界面
    """
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_sample_tasks()
        
    def init_ui(self):
        """
        初始化界面
        """
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # 标题
        title_label = QLabel("农事操作指导")
        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 当前阶段
        stage_group = QFrame()
        stage_group.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        stage_layout = QVBoxLayout(stage_group)
        
        stage_title = QLabel("当前种植阶段")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        stage_title.setFont(font)
        stage_layout.addWidget(stage_title)
        
        self.stage_label = QLabel("果实膨大期")
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.stage_label.setFont(font)
        self.stage_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stage_layout.addWidget(self.stage_label)
        
        self.stage_desc = QTextEdit()
        self.stage_desc.setMaximumHeight(80)
        self.stage_desc.setReadOnly(True)
        stage_layout.addWidget(self.stage_desc)
        
        layout.addWidget(stage_group)
        
        # 重要提醒
        reminder_group = QFrame()
        reminder_group.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        reminder_layout = QVBoxLayout(reminder_group)
        
        reminder_title = QLabel("重要提醒")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        reminder_title.setFont(font)
        reminder_layout.addWidget(reminder_title)
        
        self.reminder_text = QTextEdit()
        self.reminder_text.setMaximumHeight(100)
        self.reminder_text.setReadOnly(True)
        reminder_layout.addWidget(self.reminder_text)
        
        layout.addWidget(reminder_group)
        
        # 今日任务
        task_group = QFrame()
        task_group.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        task_layout = QVBoxLayout(task_group)
        
        task_title = QLabel("今日农事任务")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        task_title.setFont(font)
        task_layout.addWidget(task_title)
        
        # 任务网格
        self.task_grid = QGridLayout()
        self.task_grid.setSpacing(10)
        
        # 创建任务小部件
        self.task_widgets = []
        for i in range(4):
            widget = FarmingTaskWidget()
            self.task_widgets.append(widget)
            row = i // 2
            col = i % 2
            self.task_grid.addWidget(widget, row, col)
        
        task_layout.addLayout(self.task_grid)
        layout.addWidget(task_group)
        
    def load_sample_tasks(self):
        """
        加载示例任务数据
        """
        # 更新当前阶段
        self.stage_label.setText("果实膨大期")
        self.stage_desc.setPlainText(
            "果实膨大期是秋月梨果实快速生长的阶段，需要充足的水分和养分供给。"
            "此阶段应加强水肥管理，同时注意病虫害防治。"
        )
        
        # 更新重要提醒
        self.reminder_text.setPlainText(
            "1. 保持土壤湿润，但避免积水\n"
            "2. 及时追施钾肥促进果实膨大\n"
            "3. 注意防治梨小食心虫\n"
            "4. 适时进行疏果，保证果实品质"
        )
        
        # 更新任务数据
        tasks = [
            ("灌溉管理", "今天需要进行一次充分灌溉，确保土壤湿润深度达到30cm以上"),
            ("施肥作业", "追施硫酸钾复合肥，每株用量0.5kg"),
            ("病虫害检查", "全面检查果园，特别注意梨小食心虫的发生情况"),
            ("杂草清理", "清除树盘周围杂草，保持果园清洁")
        ]
        
        for i, (title, desc) in enumerate(tasks):
            if i < len(self.task_widgets):
                self.task_widgets[i].update_task(title, desc)


if __name__ == "__main__":
    # 测试代码
    app = QApplication(sys.argv)
    widget = FarmingWidget()
    widget.show()
    sys.exit(app.exec())