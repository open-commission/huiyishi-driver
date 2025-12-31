#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UART传感器数据采集器
通过串口读取真实的传感器数据
"""

import json

import serial
from PyQt6.QtCore import QTimer, QObject, pyqtSignal

from models.environment_model import EnvironmentData


class UARTSensorController(QObject):
    """
    UART传感器控制器类
    通过串口读取真实传感器数据
    """
    # 定义信号，用于通知数据更新
    data_updated = pyqtSignal(EnvironmentData)
    
    def __init__(self, port='/dev/ttyS0', baudrate=9600, parent=None):
        super().__init__(parent)
        self.port = port
        self.baudrate = baudrate
        self.serial_conn = None
        self.is_running = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.read_sensor_data)
        
    def start_monitoring(self, interval_ms: int = 5000):
        """
        开始监控传感器数据
        
        Args:
            interval_ms: 数据采集间隔（毫秒）
        """
        if not self.is_running:
            try:
                # 初始化串口连接
                self.serial_conn = serial.Serial(
                    port=self.port,
                    baudrate=self.baudrate,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=1
                )
                print(f"串口 {self.port} 连接成功，波特率 {self.baudrate}")
                
                self.timer.start(interval_ms)
                self.is_running = True
                print("UART传感器监控已启动")
            except Exception as e:
                print(f"串口连接失败: {e}")
                self.is_running = False
    
    def stop_monitoring(self):
        """
        停止监控传感器数据
        """
        if self.is_running:
            self.timer.stop()
            if self.serial_conn and self.serial_conn.is_open:
                self.serial_conn.close()
            self.is_running = False
            print("UART传感器监控已停止")
    
    def read_sensor_data(self):
        """
        读取传感器数据
        期望从串口读取JSON格式数据，例如：
        {
            "temperature": 25.5,
            "humidity": 60.0,
            "light": 5000.0,
            "occupancy": 0.6
        }
        """
        if not self.serial_conn or not self.serial_conn.is_open:
            print("串口未连接")
            return
            
        try:
            # 读取一行数据
            if self.serial_conn.in_waiting > 0:
                line = self.serial_conn.readline().decode('utf-8').strip()
                if line:
                    # 解析JSON数据
                    data = json.loads(line)
                    
                    # 创建环境数据对象
                    env_data = EnvironmentData(
                        temperature=float(data.get('temperature', 0.0)),
                        humidity=float(data.get('humidity', 0.0)),
                        light=float(data.get('light', 0.0)),
                        occupancy=float(data.get('occupancy', 0.0))
                    )
                    
                    # 发送信号通知UI更新
                    self.data_updated.emit(env_data)
                    print(f"UART传感器数据更新: {env_data.temperature}°C, "
                          f"{env_data.humidity}%, {env_data.light}lux, "
                          f"{env_data.occupancy*100:.1f}%")
                    
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
        except Exception as e:
            print(f"读取传感器数据时出错: {e}")
    
    def send_command(self, command):
        """
        向传感器发送命令
        
        Args:
            command: 要发送的命令字符串
        """
        if self.serial_conn and self.serial_conn.is_open:
            try:
                self.serial_conn.write(command.encode('utf-8'))
                print(f"发送命令: {command}")
            except Exception as e:
                print(f"发送命令失败: {e}")


# 模拟测试代码
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    
    class TestUART:
        def __init__(self):
            self.uart_controller = UARTSensorController('/dev/ttyS0', 9600)
            self.uart_controller.data_updated.connect(self.on_data_updated)
            
        def on_data_updated(self, env_data):
            print(f"接收到数据: 温度={env_data.temperature}°C, "
                  f"湿度={env_data.humidity}%, "
                  f"光照={env_data.light}lux, "
                  f"占用率={env_data.occupancy*100:.1f}%")
        
        def start(self):
            self.uart_controller.start_monitoring(1000)
    
    app = QApplication(sys.argv)
    test = TestUART()
    test.start()
    
    # 模拟运行30秒
    timer = QTimer()
    timer.timeout.connect(lambda: app.quit())
    timer.start(30000)
    
    sys.exit(app.exec())