#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
会议室设备管理界面
用于录入和查询会议室设备信息
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
    会议室设备管理界面
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
        title_label = QLabel("会议室设备管理系统")
        font = self.font()
        font.setPointSize(18)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 创建输入区域
        input_group = QGroupBox("录入设备记录")
        input_layout = QFormLayout(input_group)
        
        # 二维码输入
        self.qr_code_input = QLineEdit()
        self.qr_code_input.setPlaceholderText("请输入设备二维码")
        input_layout.addRow("二维码:", self.qr_code_input)
        
        # 设备ID输入
        self.device_id_input = QLineEdit()
        self.device_id_input.setPlaceholderText("请输入设备ID")
        input_layout.addRow("设备ID:", self.device_id_input)
        
        # 安装日期选择
        self.install_date_input = QDateEdit()
        self.install_date_input.setDate(QDate.currentDate())
        self.install_date_input.setCalendarPopup(True)
        input_layout.addRow("安装日期:", self.install_date_input)
        
        # 维护日期选择
        self.maintenance_date_input = QDateEdit()
        self.maintenance_date_input.setDate(QDate.currentDate())
        self.maintenance_date_input.setCalendarPopup(True)
        input_layout.addRow("维护日期:", self.maintenance_date_input)
        
        # 设备类型选择
        self.type_input = QComboBox()
        self.type_input.addItems(["投影仪", "音响", "空调", "照明", "门禁"])
        input_layout.addRow("设备类型:", self.type_input)
        
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
        table_group = QGroupBox("设备记录列表")
        table_layout = QVBoxLayout(table_group)
        
        self.record_table = QTableWidget()
        self.record_table.setColumnCount(7)
        self.record_table.setHorizontalHeaderLabels([
            "二维码", "设备ID", "安装日期", "维护日期", "设备类型", "备注", "创建时间"
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
                device_id="D20251001",
                qr_code="MTG20251001001",
                install_date=datetime(2025, 3, 15),
                maintenance_date=datetime(2025, 10, 10),
                device_type="投影仪",
                notes="会议室A投影仪，状态良好"
            ),
            ProductionRecord(
                device_id="D20251001",
                qr_code="MTG20251001002",
                install_date=datetime(2025, 3, 15),
                maintenance_date=datetime(2025, 10, 10),
                device_type="音响",
                notes="会议室B音响系统"
            ),
            ProductionRecord(
                device_id="D20251002",
                qr_code="MTG20251002001",
                install_date=datetime(2025, 3, 20),
                maintenance_date=datetime(2025, 10, 15),
                device_type="空调",
                notes="会议室C空调，制冷效果佳"
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
        保存设备记录
        """
        # 获取表单数据
        qr_code = self.qr_code_input.text().strip()
        device_id = self.device_id_input.text().strip()
        
        if not qr_code or not device_id:
            QMessageBox.warning(self, "警告", "二维码和设备ID不能为空！")
            return
            
        # 获取日期数据
        install_date = self.install_date_input.date().toPyDate()
        maintenance_date = self.maintenance_date_input.date().toPyDate()
        
        # 获取其他数据
        device_type = self.type_input.currentText()
        notes = self.notes_input.toPlainText().strip()
        
        # 创建设备记录对象
        record = ProductionRecord(
            device_id=device_id,
            qr_code=qr_code,
            install_date=install_date,
            maintenance_date=maintenance_date,
            device_type=device_type,
            notes=notes
        )
        
        # 保存到数据库
        try:
            self.database.save_production_record(record)
            
            # 显示成功消息
            QMessageBox.information(self, "成功", "设备记录保存成功！")
            
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
        查询设备记录
        """
        qr_code = self.qr_code_input.text().strip()
        
        if not qr_code:
            QMessageBox.warning(self, "警告", "请输入要查询的二维码！")
            return
            
        # 查询记录
        record = self.database.get_production_record(qr_code)
        
        if record:
            # 填充表单
            self.device_id_input.setText(record.device_id)
            self.install_date_input.setDate(record.install_date)
            
            if record.maintenance_date:
                self.maintenance_date_input.setDate(record.maintenance_date)
                
            # 设置设备类型
            types = [self.type_input.itemText(i) for i in range(self.type_input.count())]
            if record.device_type in types:
                self.type_input.setCurrentText(record.device_type)
                
            self.notes_input.setPlainText(record.notes)
            
            QMessageBox.information(self, "查询结果", f"找到二维码为 {qr_code} 的记录")
        else:
            QMessageBox.warning(self, "查询结果", f"未找到二维码为 {qr_code} 的记录")
            
    def delete_record(self):
        """
        删除设备记录
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
        self.device_id_input.clear()
        self.install_date_input.setDate(QDate.currentDate())
        self.maintenance_date_input.setDate(QDate.currentDate())
        self.type_input.setCurrentIndex(0)
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
            self.record_table.setItem(row, 1, QTableWidgetItem(record.device_id))
            
                # 格式化日期显示
            install_date_str = record.install_date.strftime("%Y-%m-%d") if record.install_date else ""
            self.record_table.setItem(row, 2, QTableWidgetItem(install_date_str))
            
            maintenance_date_str = record.maintenance_date.strftime("%Y-%m-%d") if record.maintenance_date else ""
            self.record_table.setItem(row, 3, QTableWidgetItem(maintenance_date_str))
            
            self.record_table.setItem(row, 4, QTableWidgetItem(record.device_type))
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

    def load_sample_data(self):
        """
        加载示例数据
        """
        # 创建一些示例记录
        sample_records = [
            ProductionRecord(
                device_id="D20251001",
                qr_code="MTG20251001001",
                install_date=datetime(2025, 3, 15),
                maintenance_date=datetime(2025, 10, 10),
                device_type="投影仪",
                notes="会议室A投影仪，状态良好"
            ),
            ProductionRecord(
                device_id="D20251001",
                qr_code="MTG20251001002",
                install_date=datetime(2025, 3, 15),
                maintenance_date=datetime(2025, 10, 10),
                device_type="音响",
                notes="会议室B音响系统"
            ),
            ProductionRecord(
                device_id="D20251002",
                qr_code="MTG20251002001",
                install_date=datetime(2025, 3, 20),
                maintenance_date=datetime(2025, 10, 15),
                device_type="空调",
                notes="会议室C空调，制冷效果佳"
            )
        ]
        
        for record in sample_records:
            try:
                self.database.save_production_record(record)
            except Exception as e:
                print(f"保存示例数据时出错: {e}")
            
        self.refresh_table()


if __name__ == "__main__":
    # 测试代码
    app = QApplication(sys.argv)
    widget = ProductionWidget()
    widget.show()
    sys.exit(app.exec())