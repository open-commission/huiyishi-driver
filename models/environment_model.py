#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
环境数据模型
包含温度、湿度、光照、土壤湿度等传感器数据
"""

from datetime import datetime
from typing import Dict, Any


class EnvironmentData:
    """
    环境数据模型类
    """
    def __init__(self, temperature: float = 0.0, humidity: float = 0.0, 
                 light: float = 0.0, soil_moisture: float = 0.0):
        """
        初始化环境数据
        
        Args:
            temperature: 温度 (摄氏度)
            humidity: 湿度 (%RH)
            light: 光照强度 (lux)
            soil_moisture: 土壤湿度 (%)
        """
        self.timestamp = datetime.now()
        self.temperature = temperature
        self.humidity = humidity
        self.light = light
        self.soil_moisture = soil_moisture
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将环境数据转换为字典格式
        
        Returns:
            dict: 包含所有环境数据的字典
        """
        return {
            'timestamp': self.timestamp.isoformat(),
            'temperature': self.temperature,
            'humidity': self.humidity,
            'light': self.light,
            'soil_moisture': self.soil_moisture
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EnvironmentData':
        """
        从字典创建环境数据对象
        
        Args:
            data: 包含环境数据的字典
            
        Returns:
            EnvironmentData: 环境数据对象
        """
        env_data = cls(
            temperature=data.get('temperature', 0.0),
            humidity=data.get('humidity', 0.0),
            light=data.get('light', 0.0),
            soil_moisture=data.get('soil_moisture', 0.0)
        )
        if 'timestamp' in data:
            env_data.timestamp = datetime.fromisoformat(data['timestamp'])
        return env_data


class EnvironmentHistory:
    """
    环境数据历史记录
    """
    def __init__(self):
        self.history = []
    
    def add_record(self, data: EnvironmentData):
        """
        添加环境数据记录
        
        Args:
            data: EnvironmentData 对象
        """
        self.history.append(data)
        # 只保留最近100条记录
        if len(self.history) > 100:
            self.history.pop(0)
    
    def get_recent_records(self, count: int = 10) -> list:
        """
        获取最近的环境数据记录
        
        Args:
            count: 要获取的记录数量
            
        Returns:
            list: 最近的环境数据记录列表
        """
        return self.history[-count:] if self.history else []