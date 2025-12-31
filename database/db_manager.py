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
# 不再需要导入ProductionRecord，会议室记录直接用元组处理


class DatabaseManager:
    """
    SQLite数据库管理器
    """
    def __init__(self, db_path: str = "meeting_room.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """
        初始化数据库表
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 创建会议室环境数据表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS environment_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    temperature REAL NOT NULL,
                    humidity REAL NOT NULL,
                    light REAL NOT NULL,
                    co2 REAL NOT NULL,
                    pm25 REAL NOT NULL
                )
            ''')
            
            # 创建会议室记录表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS meeting_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    room_id TEXT NOT NULL,
                    meeting_id TEXT UNIQUE NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT,
                    organizer TEXT,
                    participants TEXT,
                    notes TEXT,
                    created_at TEXT NOT NULL
                )
            ''')
            
            conn.commit()
    
    def save_environment_data(self, env_data: EnvironmentData):
        """
        保存会议室环境数据到数据库
        
        Args:
            env_data: EnvironmentData对象
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO environment_data 
                (timestamp, temperature, humidity, light, co2, pm25)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                env_data.timestamp.isoformat(),
                env_data.temperature,
                env_data.humidity,
                env_data.light,
                env_data.co2,
                env_data.pm25
            ))
            conn.commit()
    
    def get_environment_history(self, limit: int = 100) -> List[EnvironmentData]:
        """
        获取会议室环境数据历史记录
        
        Args:
            limit: 返回记录数量限制
            
        Returns:
            List[EnvironmentData]: 环境数据历史记录列表
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT timestamp, temperature, humidity, light, co2, pm25
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
                    co2=row[4],
                    pm25=row[5]
                )
                env_data.timestamp = datetime.fromisoformat(row[0])
                result.append(env_data)
            
            # 按时间顺序排列
            result.reverse()
            return result
    
    def save_meeting_record(self, room_id: str, meeting_id: str, start_time: datetime, 
                             end_time: Optional[datetime] = None, organizer: str = "", 
                             participants: str = "", notes: str = ""):
        """
        保存会议室记录到数据库
        
        Args:
            room_id: 会议室ID
            meeting_id: 会议ID
            start_time: 开始时间
            end_time: 结束时间
            organizer: 组织者
            participants: 参与者
            notes: 备注
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO meeting_records 
                (room_id, meeting_id, start_time, end_time, organizer, participants, notes, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                room_id,
                meeting_id,
                start_time.isoformat(),
                end_time.isoformat() if end_time else None,
                organizer,
                participants,
                notes,
                datetime.now().isoformat()
            ))
            conn.commit()
    
    def get_meeting_record(self, meeting_id: str) -> Optional[tuple]:
        """
        根据会议ID获取会议室记录
        
        Args:
            meeting_id: 会议ID
            
        Returns:
            tuple: 会议室记录数据，如果不存在则返回None
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT room_id, meeting_id, start_time, end_time, organizer, participants, notes, created_at
                FROM meeting_records
                WHERE meeting_id = ?
            ''', (meeting_id,))
            
            row = cursor.fetchone()
            if row:
                return row
            
            return None
    
    def get_all_meeting_records(self) -> List[tuple]:
        """
        获取所有会议室记录
        
        Returns:
            List[tuple]: 所有会议室记录列表
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT room_id, meeting_id, start_time, end_time, organizer, participants, notes, created_at
                FROM meeting_records
                ORDER BY created_at DESC
            ''')
            
            rows = cursor.fetchall()
            return rows
    
    def delete_meeting_record(self, meeting_id: str) -> bool:
        """
        删除会议室记录
        
        Args:
            meeting_id: 会议ID
            
        Returns:
            bool: 删除成功返回True，否则返回False
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM meeting_records
                WHERE meeting_id = ?
            ''', (meeting_id,))
            
            conn.commit()
            return cursor.rowcount > 0


# 测试代码
if __name__ == "__main__":
    # 创建数据库管理器实例
    db = DatabaseManager()
    
    # 测试会议室环境数据存储
    env_data = EnvironmentData(
        temperature=25.5,
        humidity=60.0,
        light=500.0,
        co2=800.0,
        pm25=15.0
    )
    db.save_environment_data(env_data)
    
    # 测试获取历史记录
    history = db.get_environment_history(10)
    print(f"获取到 {len(history)} 条环境记录")
    
    # 测试会议室记录存储
    from datetime import datetime
    db.save_meeting_record(
        room_id="MR001",
        meeting_id="MTG001",
        start_time=datetime.now(),
        organizer="张三",
        participants="李四,王五",
        notes="项目讨论会议"
    )
    
    # 测试获取会议室记录
    record = db.get_meeting_record("MTG001")
    if record:
        print(f"找到会议记录: {record[1]}, 组织者: {record[4]}")
    
    print("数据库测试完成")