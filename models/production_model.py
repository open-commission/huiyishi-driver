#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
生产溯源数据模型
包含批次、种植日期、出厂日期、水果分级等信息
"""

from datetime import datetime
from typing import Dict, Any, Optional


class ProductionRecord:
    """
    生产记录模型类
    """
    def __init__(self, batch_id: str = "", qr_code: str = "",
                 planting_date: Optional[datetime] = None,
                 harvest_date: Optional[datetime] = None,
                 grade: str = "", notes: str = ""):
        """
        初始化生产记录
        
        Args:
            batch_id: 批次号
            qr_code: 二维码
            planting_date: 种植日期
            harvest_date: 出厂日期
            grade: 水果分级
            notes: 备注信息
        """
        self.batch_id = batch_id
        self.qr_code = qr_code
        self.planting_date = planting_date if planting_date else datetime.now()
        self.harvest_date = harvest_date
        self.grade = grade
        self.notes = notes
        self.created_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将生产记录转换为字典格式
        
        Returns:
            dict: 包含所有生产记录数据的字典
        """
        return {
            'batch_id': self.batch_id,
            'qr_code': self.qr_code,
            'planting_date': self.planting_date.isoformat() if self.planting_date else None,
            'harvest_date': self.harvest_date.isoformat() if self.harvest_date else None,
            'grade': self.grade,
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProductionRecord':
        """
        从字典创建生产记录对象
        
        Args:
            data: 包含生产记录数据的字典
            
        Returns:
            ProductionRecord: 生产记录对象
        """
        record = cls(
            batch_id=data.get('batch_id', ''),
            qr_code=data.get('qr_code', ''),
            grade=data.get('grade', ''),
            notes=data.get('notes', '')
        )
        
        if 'planting_date' in data and data['planting_date']:
            record.planting_date = datetime.fromisoformat(data['planting_date'])
        
        if 'harvest_date' in data and data['harvest_date']:
            record.harvest_date = datetime.fromisoformat(data['harvest_date'])
            
        if 'created_at' in data and data['created_at']:
            record.created_at = datetime.fromisoformat(data['created_at'])
            
        return record


class ProductionDatabase:
    """
    生产记录数据库
    """
    def __init__(self):
        self.records = {}
    
    def add_record(self, record: ProductionRecord):
        """
        添加生产记录
        
        Args:
            record: ProductionRecord 对象
        """
        self.records[record.qr_code] = record
    
    def get_record(self, qr_code: str) -> Optional[ProductionRecord]:
        """
        根据二维码获取生产记录
        
        Args:
            qr_code: 二维码
            
        Returns:
            ProductionRecord: 生产记录对象，如果不存在则返回None
        """
        return self.records.get(qr_code)
    
    def get_all_records(self) -> Dict[str, ProductionRecord]:
        """
        获取所有生产记录
        
        Returns:
            dict: 所有生产记录
        """
        return self.records.copy()
    
    def delete_record(self, qr_code: str) -> bool:
        """
        删除生产记录
        
        Args:
            qr_code: 二维码
            
        Returns:
            bool: 删除成功返回True，否则返回False
        """
        if qr_code in self.records:
            del self.records[qr_code]
            return True
        return False