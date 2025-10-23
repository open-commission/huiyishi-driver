#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
传感器控制器
模拟传感器数据读取和处理
"""

import random
import time
from typing import Callable
from PyQt6.QtCore import QTimer, QObject, pyqtSignal
from models.environment_model import EnvironmentData
from database.db_manager import DatabaseManager
from config import config

# 条件导入UART传感器控制器
try:
    from hardware.uart_sensor import UARTSensorController
    UART_AVAILABLE = True
except ImportError:
    UARTSensorController = None
    UART_AVAILABLE = False


class SensorController(QObject):
    """
    传感器控制器类
    负责处理传感器数据采集和处理
    """
    # 定义信号，用于通知UI更新
    data_updated = pyqtSignal(EnvironmentData)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_manager = DatabaseManager()
        self.is_running = False
        
        # 根据环境配置选择数据源
        if config.is_production() and UART_AVAILABLE:
            # 生产环境使用真实的UART传感器
            self.data_source = "uart"
            self.uart_controller = UARTSensorController(
                port=config.uart_port,
                baudrate=config.uart_baudrate
            )
            self.uart_controller.data_updated.connect(self.on_uart_data_updated)
        else:
            # 开发环境使用模拟数据
            self.data_source = "simulated"
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.generate_simulated_data)
            
            # 模拟传感器初始值
            self.temperature = 25.0
            self.humidity = 60.0
            self.light = 5000.0
            self.soil_moisture = 70.0
    
    def start_monitoring(self, interval_ms: int = 5000):
        """
        开始监控传感器数据
        
        Args:
            interval_ms: 数据采集间隔（毫秒）
        """
        if not self.is_running:
            if self.data_source == "uart":
                self.uart_controller.start_monitoring(interval_ms)
            else:
                self.timer.start(interval_ms)
            self.is_running = True
    
    def stop_monitoring(self):
        """
        停止监控传感器数据
        """
        if self.is_running:
            if self.data_source == "uart":
                self.uart_controller.stop_monitoring()
            else:
                self.timer.stop()
            self.is_running = False
    
    def generate_simulated_data(self):
        """
        生成模拟传感器数据（用于开发环境）
        """
        # 模拟传感器数据波动
        self.temperature += random.uniform(-0.5, 0.5)
        self.humidity += random.uniform(-1.0, 1.0)
        self.light += random.uniform(-100.0, 100.0)
        self.soil_moisture += random.uniform(-2.0, 2.0)
        
        # 限制数据范围
        self.temperature = max(0, min(40, self.temperature))
        self.humidity = max(0, min(100, self.humidity))
        self.light = max(0, min(100000, self.light))
        self.soil_moisture = max(0, min(100, self.soil_moisture))
        
        # 创建环境数据对象
        env_data = EnvironmentData(
            temperature=round(self.temperature, 2),
            humidity=round(self.humidity, 2),
            light=round(self.light, 2),
            soil_moisture=round(self.soil_moisture, 2)
        )
        
        # 保存到数据库
        self.db_manager.save_environment_data(env_data)
        
        # 发送信号通知UI更新
        self.data_updated.emit(env_data)
    
    def on_uart_data_updated(self, env_data: EnvironmentData):
        """
        处理UART传感器数据更新
        
        Args:
            env_data: EnvironmentData对象
        """
        # 保存到数据库
        self.db_manager.save_environment_data(env_data)
        
        # 发送信号通知UI更新
        self.data_updated.emit(env_data)
    
    def get_current_data(self) -> EnvironmentData:
        """
        获取当前传感器数据
        
        Returns:
            EnvironmentData: 当前环境数据
        """
        if self.data_source == "uart":
            # 对于UART传感器，我们不存储当前值，直接从数据库获取最新数据
            history = self.db_manager.get_environment_history(1)
            if history:
                return history[0]
            else:
                return EnvironmentData()
        else:
            # 对于模拟数据，返回当前值
            return EnvironmentData(
                temperature=self.temperature,
                humidity=self.humidity,
                light=self.light,
                soil_moisture=self.soil_moisture
            )
    
    def get_history_data(self, limit: int = 100) -> list:
        """
        获取历史传感器数据
        
        Args:
            limit: 返回记录数量限制
            
        Returns:
            list: 历史环境数据列表
        """
        return self.db_manager.get_environment_history(limit)


class ServoController(QObject):
    """
    舵机控制器类
    控制舵机开关状态
    """
    # 定义信号，用于通知UI状态变化
    status_changed = pyqtSignal(bool)  # True表示开启，False表示关闭
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_active = False
    
    def toggle_servo(self):
        """
        切换舵机状态
        """
        self.is_active = not self.is_active
        self.status_changed.emit(self.is_active)
        return self.is_active
    
    def get_status(self) -> bool:
        """
        获取舵机当前状态
        
        Returns:
            bool: 舵机状态，True表示开启，False表示关闭
        """
        return self.is_active
    
    def activate_servo(self):
        """
        激活舵机
        """
        self.is_active = True
        self.status_changed.emit(True)
    
    def deactivate_servo(self):
        """
        关闭舵机
        """
        self.is_active = False
        self.status_changed.emit(False)