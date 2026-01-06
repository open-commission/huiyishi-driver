#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
会议室环境数据模型
包含温度、湿度、光照、二氧化碳、PM2.5、占用率等传感器数据
"""

from datetime import datetime
from typing import Dict, Any


class EnvironmentData:
    """
    会议室环境数据模型类
    """
    def __init__(self, temperature: float = 0.0, humidity: float = 0.0, 
                 light: float = 0.0, co2: float = 0.0, pm25: float = 0.0,
                 occupancy: float = 0.0, motor_status: bool = False, servo_status: bool = False):
        """
        初始化会议室环境数据
        
        Args:
            temperature: 温度 (摄氏度)
            humidity: 湿度 (%RH)
            light: 光照强度 (lux)
            co2: 二氧化碳浓度 (ppm)
            pm25: PM2.5浓度 (μg/m³)
            occupancy: 会议室占用率 (0.0-1.0)
            motor_status: 电机状态 (现场从机)
            servo_status: 舵机状态 (会议室从机)
        """
        self.timestamp = datetime.now()
        self.temperature = temperature
        self.humidity = humidity
        self.light = light
        self.co2 = co2
        self.pm25 = pm25
        self.occupancy = occupancy
        self.motor_status = motor_status  # 现场从机电机状态
        self.servo_status = servo_status  # 会议室从机舵机状态
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将会议室环境数据转换为字典格式
        
        Returns:
            dict: 包含所有环境数据的字典
        """
        return {
            'timestamp': self.timestamp.isoformat(),
            'temperature': self.temperature,
            'humidity': self.humidity,
            'light': self.light,
            'co2': self.co2,
            'pm25': self.pm25,
            'occupancy': self.occupancy,
            'motor_status': self.motor_status,
            'servo_status': self.servo_status
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EnvironmentData':
        """
        从字典创建会议室环境数据对象
        
        Args:
            data: 包含环境数据的字典
            
        Returns:
            EnvironmentData: 环境数据对象
        """
        env_data = cls(
            temperature=data.get('temperature', 0.0),
            humidity=data.get('humidity', 0.0),
            light=data.get('light', 0.0),
            co2=data.get('co2', 0.0),
            pm25=data.get('pm25', 0.0),
            occupancy=data.get('occupancy', 0.0),
            motor_status=data.get('motor_status', False),
            servo_status=data.get('servo_status', False)
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