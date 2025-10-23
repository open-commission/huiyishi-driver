#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
生产溯源管理界面
用于录入和查询生产记录
"""

import sys
from datetime import datetime
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLineEdit, QPushButton, QTextEdit, QTableWidget,
                             QTableWidgetItem, QLabel, QMessageBox, QDateEdit,
                             QComboBox, QHeaderView, QGroupBox, QApplication)
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from models.production_model import ProductionRecord
from database.db_manager import DatabaseManager


class ProductionWidget(QWidget):
    """
    生产溯源管理界面
    """
    # 定义信号
    data_updated = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.database = DatabaseManager()
        self.current_record = None
        self.init_ui()
        self.load_sample_data()
        
    def init_ui(self):
        """
        初始化界面
        """
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # 标题
        title_label = QLabel("秋月梨生产溯源管理系统")
        font = self.font()
        font.setPointSize(18)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 创建输入区域
        input_group = QGroupBox("录入生产记录")
        input_layout = QFormLayout(input_group)
        
        # 二维码输入
        self.qr_code_input = QLineEdit()
        self.qr_code_input.setPlaceholderText("请输入产品二维码")
        input_layout.addRow("二维码:", self.qr_code_input)
        
        # 批次号输入
        self.batch_id_input = QLineEdit()
        self.batch_id_input.setPlaceholderText("请输入批次号")
        input_layout.addRow("批次号:", self.batch_id_input)
        
        # 种植日期选择
        self.planting_date_input = QDateEdit()
        self.planting_date_input.setDate(QDate.currentDate())
        self.planting_date_input.setCalendarPopup(True)
        input_layout.addRow("种植日期:", self.planting_date_input)
        
        # 出厂日期选择
        self.harvest_date_input = QDateEdit()
        self.harvest_date_input.setDate(QDate.currentDate())
        self.harvest_date_input.setCalendarPopup(True)
        input_layout.addRow("出厂日期:", self.harvest_date_input)
        
        # 水果分级选择
        self.grade_input = QComboBox()
        self.grade_input.addItems(["特级", "一级", "二级", "三级"])
        input_layout.addRow("水果分级:", self.grade_input)
        
        # 备注输入
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(60)
        self.notes_input.setPlaceholderText("请输入备注信息...")
        input_layout.addRow("备注:", self.notes_input)
        
        layout.addWidget(input_group)
        
        # 创建按钮区域
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton("保存记录")
        self.save_button.clicked.connect(self.save_record)
        
        self.query_button = QPushButton("查询记录")
        self.query_button.clicked.connect(self.query_record)
        
        self.clear_button = QPushButton("清空表单")
        self.clear_button.clicked.connect(self.clear_form)
        
        self.delete_button = QPushButton("删除记录")
        self.delete_button.clicked.connect(self.delete_record)
        
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.query_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.delete_button)
        
        layout.addLayout(button_layout)
        
        # 创建表格显示区域
        table_group = QGroupBox("生产记录列表")
        table_layout = QVBoxLayout(table_group)
        
        self.record_table = QTableWidget()
        self.record_table.setColumnCount(7)
        self.record_table.setHorizontalHeaderLabels([
            "二维码", "批次号", "种植日期", "出厂日期", "水果分级", "备注", "创建时间"
        ])
        
        # 设置表格属性
        self.record_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # 禁止编辑
        self.record_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)  # 整行选择
        self.record_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.record_table.verticalHeader().setVisible(False)
        self.record_table.setAlternatingRowColors(True)
        
        # 连接表格点击事件
        self.record_table.cellClicked.connect(self.on_table_cell_clicked)
        
        table_layout.addWidget(self.record_table)
        layout.addWidget(table_group)
        
        # 加载所有记录
        self.refresh_table()
        
    def load_sample_data(self):
        """
        加载示例数据
        """
        # 创建一些示例记录
        sample_records = [
            ProductionRecord(
                batch_id="P20251001",
                qr_code="QYLP20251001001",
                planting_date=datetime(2025, 3, 15),
                harvest_date=datetime(2025, 10, 10),
                grade="特级",
                notes="第一批秋月梨，品质优良"
            ),
            ProductionRecord(
                batch_id="P20251001",
                qr_code="QYLP20251001002",
                planting_date=datetime(2025, 3, 15),
                harvest_date=datetime(2025, 10, 10),
                grade="一级",
                notes="第二批秋月梨"
            ),
            ProductionRecord(
                batch_id="P20251002",
                qr_code="QYLP20251002001",
                planting_date=datetime(2025, 3, 20),
                harvest_date=datetime(2025, 10, 15),
                grade="特级",
                notes="第三批秋月梨，糖分含量高"
            )
        ]
        
        for record in sample_records:
            try:
                self.database.save_production_record(record)
            except Exception as e:
                print(f"保存示例数据时出错: {e}")
            
        self.refresh_table()
        
    def save_record(self):
        """
        保存生产记录
        """
        # 获取表单数据
        qr_code = self.qr_code_input.text().strip()
        batch_id = self.batch_id_input.text().strip()
        
        if not qr_code or not batch_id:
            QMessageBox.warning(self, "警告", "二维码和批次号不能为空！")
            return
            
        # 获取日期数据
        planting_date = self.planting_date_input.date().toPyDate()
        harvest_date = self.harvest_date_input.date().toPyDate()
        
        # 获取其他数据
        grade = self.grade_input.currentText()
        notes = self.notes_input.toPlainText().strip()
        
        # 创建生产记录对象
        record = ProductionRecord(
            batch_id=batch_id,
            qr_code=qr_code,
            planting_date=planting_date,
            harvest_date=harvest_date,
            grade=grade,
            notes=notes
        )
        
        # 保存到数据库
        try:
            self.database.save_production_record(record)
            
            # 显示成功消息
            QMessageBox.information(self, "成功", "生产记录保存成功！")
            
            # 清空表单
            self.clear_form()
            
            # 刷新表格
            self.refresh_table()
            
            # 发出数据更新信号
            self.data_updated.emit()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存记录时出错: {str(e)}")
        
    def query_record(self):
        """
        查询生产记录
        """
        qr_code = self.qr_code_input.text().strip()
        
        if not qr_code:
            QMessageBox.warning(self, "警告", "请输入要查询的二维码！")
            return
            
        # 查询记录
        record = self.database.get_production_record(qr_code)
        
        if record:
            # 填充表单
            self.batch_id_input.setText(record.batch_id)
            self.planting_date_input.setDate(record.planting_date)
            
            if record.harvest_date:
                self.harvest_date_input.setDate(record.harvest_date)
                
            # 设置分级
            grades = [self.grade_input.itemText(i) for i in range(self.grade_input.count())]
            if record.grade in grades:
                self.grade_input.setCurrentText(record.grade)
                
            self.notes_input.setPlainText(record.notes)
            
            QMessageBox.information(self, "查询结果", f"找到二维码为 {qr_code} 的记录")
        else:
            QMessageBox.warning(self, "查询结果", f"未找到二维码为 {qr_code} 的记录")
            
    def delete_record(self):
        """
        删除生产记录
        """
        qr_code = self.qr_code_input.text().strip()
        
        if not qr_code:
            QMessageBox.warning(self, "警告", "请输入要删除的记录二维码！")
            return
            
        reply = QMessageBox.question(self, "确认删除", 
                                   f"确定要删除二维码为 {qr_code} 的记录吗？",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            success = self.database.delete_production_record(qr_code)
            
            if success:
                QMessageBox.information(self, "成功", "记录删除成功！")
                self.clear_form()
                self.refresh_table()
                self.data_updated.emit()
            else:
                QMessageBox.warning(self, "错误", "未找到指定的记录！")
                
    def clear_form(self):
        """
        清空表单
        """
        self.qr_code_input.clear()
        self.batch_id_input.clear()
        self.planting_date_input.setDate(QDate.currentDate())
        self.harvest_date_input.setDate(QDate.currentDate())
        self.grade_input.setCurrentIndex(0)
        self.notes_input.clear()
        self.current_record = None
        
    def refresh_table(self):
        """
        刷新表格数据
        """
        # 清空表格
        self.record_table.setRowCount(0)
        
        # 获取所有记录
        records = self.database.get_all_production_records()
        
        # 添加记录到表格
        self.record_table.setRowCount(len(records))
        
        for row, record in enumerate(records):
            self.record_table.setItem(row, 0, QTableWidgetItem(record.qr_code))
            self.record_table.setItem(row, 1, QTableWidgetItem(record.batch_id))
            
            # 格式化日期显示
            planting_date_str = record.planting_date.strftime("%Y-%m-%d") if record.planting_date else ""
            self.record_table.setItem(row, 2, QTableWidgetItem(planting_date_str))
            
            harvest_date_str = record.harvest_date.strftime("%Y-%m-%d") if record.harvest_date else ""
            self.record_table.setItem(row, 3, QTableWidgetItem(harvest_date_str))
            
            self.record_table.setItem(row, 4, QTableWidgetItem(record.grade))
            self.record_table.setItem(row, 5, QTableWidgetItem(record.notes))
            
            created_at_str = record.created_at.strftime("%Y-%m-%d %H:%M") if record.created_at else ""
            self.record_table.setItem(row, 6, QTableWidgetItem(created_at_str))
            
    def on_table_cell_clicked(self, row, column):
        """
        处理表格单元格点击事件
        
        Args:
            row: 行索引
            column: 列索引
        """
        # 获取该行的二维码
        qr_code_item = self.record_table.item(row, 0)
        if qr_code_item:
            qr_code = qr_code_item.text()
            self.qr_code_input.setText(qr_code)
            self.query_record()


if __name__ == "__main__":
    # 测试代码
    app = QApplication(sys.argv)
    widget = ProductionWidget()
    widget.show()
    sys.exit(app.exec())