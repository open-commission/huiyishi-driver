#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
数据库管理器
用于管理SQLite数据库连接和操作
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Optional
from models.environment_model import EnvironmentData
from models.production_model import ProductionRecord


class DatabaseManager:
    """
    SQLite数据库管理器
    """
    def __init__(self, db_path: str = "qiuyue.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """
        初始化数据库表
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 创建环境数据表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS environment_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    temperature REAL NOT NULL,
                    humidity REAL NOT NULL,
                    light REAL NOT NULL,
                    soil_moisture REAL NOT NULL
                )
            ''')
            
            # 创建生产记录表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS production_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    batch_id TEXT NOT NULL,
                    qr_code TEXT UNIQUE NOT NULL,
                    planting_date TEXT NOT NULL,
                    harvest_date TEXT,
                    grade TEXT,
                    notes TEXT,
                    created_at TEXT NOT NULL
                )
            ''')
            
            conn.commit()
    
    def save_environment_data(self, env_data: EnvironmentData):
        """
        保存环境数据到数据库
        
        Args:
            env_data: EnvironmentData对象
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO environment_data 
                (timestamp, temperature, humidity, light, soil_moisture)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                env_data.timestamp.isoformat(),
                env_data.temperature,
                env_data.humidity,
                env_data.light,
                env_data.soil_moisture
            ))
            conn.commit()
    
    def get_environment_history(self, limit: int = 100) -> List[EnvironmentData]:
        """
        获取环境数据历史记录
        
        Args:
            limit: 返回记录数量限制
            
        Returns:
            List[EnvironmentData]: 环境数据历史记录列表
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT timestamp, temperature, humidity, light, soil_moisture
                FROM environment_data
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            result = []
            for row in rows:
                env_data = EnvironmentData(
                    temperature=row[1],
                    humidity=row[2],
                    light=row[3],
                    soil_moisture=row[4]
                )
                env_data.timestamp = datetime.fromisoformat(row[0])
                result.append(env_data)
            
            # 按时间顺序排列
            result.reverse()
            return result
    
    def save_production_record(self, record: ProductionRecord):
        """
        保存生产记录到数据库
        
        Args:
            record: ProductionRecord对象
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO production_records 
                (batch_id, qr_code, planting_date, harvest_date, grade, notes, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                record.batch_id,
                record.qr_code,
                record.planting_date.isoformat(),
                record.harvest_date.isoformat() if record.harvest_date else None,
                record.grade,
                record.notes,
                record.created_at.isoformat()
            ))
            conn.commit()
    
    def get_production_record(self, qr_code: str) -> Optional[ProductionRecord]:
        """
        根据二维码获取生产记录
        
        Args:
            qr_code: 产品二维码
            
        Returns:
            ProductionRecord: 生产记录对象，如果不存在则返回None
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT batch_id, qr_code, planting_date, harvest_date, grade, notes, created_at
                FROM production_records
                WHERE qr_code = ?
            ''', (qr_code,))
            
            row = cursor.fetchone()
            if row:
                record = ProductionRecord(
                    batch_id=row[0],
                    qr_code=row[1],
                    grade=row[4],
                    notes=row[5]
                )
                record.planting_date = datetime.fromisoformat(row[2])
                if row[3]:
                    record.harvest_date = datetime.fromisoformat(row[3])
                record.created_at = datetime.fromisoformat(row[6])
                return record
            
            return None
    
    def get_all_production_records(self) -> List[ProductionRecord]:
        """
        获取所有生产记录
        
        Returns:
            List[ProductionRecord]: 所有生产记录列表
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT batch_id, qr_code, planting_date, harvest_date, grade, notes, created_at
                FROM production_records
                ORDER BY created_at DESC
            ''')
            
            rows = cursor.fetchall()
            result = []
            for row in rows:
                record = ProductionRecord(
                    batch_id=row[0],
                    qr_code=row[1],
                    grade=row[4],
                    notes=row[5]
                )
                record.planting_date = datetime.fromisoformat(row[2])
                if row[3]:
                    record.harvest_date = datetime.fromisoformat(row[3])
                record.created_at = datetime.fromisoformat(row[6])
                result.append(record)
            
            return result
    
    def delete_production_record(self, qr_code: str) -> bool:
        """
        删除生产记录
        
        Args:
            qr_code: 产品二维码
            
        Returns:
            bool: 删除成功返回True，否则返回False
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM production_records
                WHERE qr_code = ?
            ''', (qr_code,))
            
            conn.commit()
            return cursor.rowcount > 0


# 测试代码
if __name__ == "__main__":
    # 创建数据库管理器实例
    db = DatabaseManager()
    
    # 测试环境数据存储
    env_data = EnvironmentData(
        temperature=25.5,
        humidity=60.0,
        light=5000.0,
        soil_moisture=70.0
    )
    db.save_environment_data(env_data)
    
    # 测试获取历史记录
    history = db.get_environment_history(10)
    print(f"获取到 {len(history)} 条环境记录")
    
    # 测试生产记录存储
    prod_record = ProductionRecord(
        batch_id="TEST001",
        qr_code="QR001",
        grade="特级",
        notes="测试记录"
    )
    db.save_production_record(prod_record)
    
    # 测试获取生产记录
    record = db.get_production_record("QR001")
    if record:
        print(f"找到记录: {record.qr_code}, 等级: {record.grade}")
    
    print("数据库测试完成")