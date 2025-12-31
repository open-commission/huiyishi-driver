#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
设备管理数据模型
包含设备ID、安装日期、维护日期、设备类型等信息
"""

from datetime import datetime
from typing import Dict, Any, Optional


class ProductionRecord:
    """
    设备记录模型类
    """
    def __init__(self, device_id: str = "", qr_code: str = "",
                 install_date: Optional[datetime] = None,
                 maintenance_date: Optional[datetime] = None,
                 device_type: str = "", notes: str = ""):
        """
        初始化设备记录
        
        Args:
            device_id: 设备ID
            qr_code: 二维码
            install_date: 安装日期
            maintenance_date: 维护日期
            device_type: 设备类型
            notes: 备注信息
        """
        self.device_id = device_id
        self.qr_code = qr_code
        self.install_date = install_date if install_date else datetime.now()
        self.maintenance_date = maintenance_date
        self.device_type = device_type
        self.notes = notes
        self.created_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将设备记录转换为字典格式
        
        Returns:
            dict: 包含所有设备记录数据的字典
        """
        return {
            'device_id': self.device_id,
            'qr_code': self.qr_code,
            'install_date': self.install_date.isoformat() if self.install_date else None,
            'maintenance_date': self.maintenance_date.isoformat() if self.maintenance_date else None,
            'device_type': self.device_type,
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProductionRecord':
        """
        从字典创建设备记录对象
        
        Args:
            data: 包含设备记录数据的字典
            
        Returns:
            ProductionRecord: 设备记录对象
        """
        record = cls(
            device_id=data.get('device_id', ''),
            qr_code=data.get('qr_code', ''),
            device_type=data.get('device_type', ''),
            notes=data.get('notes', '')
        )
        
        if 'install_date' in data and data['install_date']:
            record.install_date = datetime.fromisoformat(data['install_date'])
        
        if 'maintenance_date' in data and data['maintenance_date']:
            record.maintenance_date = datetime.fromisoformat(data['maintenance_date'])
            
        if 'created_at' in data and data['created_at']:
            record.created_at = datetime.fromisoformat(data['created_at'])
            
        return record


class ProductionDatabase:
    """
    设备记录数据库
    """
    def __init__(self):
        self.records = {}
    
    def add_record(self, record: ProductionRecord):
        """
        添加设备记录
        
        Args:
            record: ProductionRecord 对象
        """
        self.records[record.qr_code] = record
    
    def get_record(self, qr_code: str) -> Optional[ProductionRecord]:
        """
        根据二维码获取设备记录
        
        Args:
            qr_code: 二维码
            
        Returns:
            ProductionRecord: 设备记录对象，如果不存在则返回None
        """
        return self.records.get(qr_code)
    
    def get_all_records(self) -> Dict[str, ProductionRecord]:
        """
        获取所有设备记录
        
        Returns:
            dict: 所有设备记录
        """
        return self.records.copy()
    
    def delete_record(self, qr_code: str) -> bool:
        """
        删除设备记录
        
        Args:
            qr_code: 二维码
            
        Returns:
            bool: 删除成功返回True，否则返回False
        """
        if qr_code in self.records:
            del self.records[qr_code]
            return True
        return False