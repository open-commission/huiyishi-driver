#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
系统配置文件
用于管理开发环境和生产环境的配置
"""

import os


class Config:
    """
    系统配置类
    """
    def __init__(self):
        # 环境配置
        self.environment = os.getenv('APP_ENV', 'development')  # development or production
        
        # GPIO配置
        self.gpio_enabled = self.environment == 'production'
        
        # UART配置
        self.uart_port = os.getenv('UART_PORT', '/dev/ttyS0')  # 默认串口
        self.uart_baudrate = int(os.getenv('UART_BAUDRATE', '9600'))  # 默认波特率
        
        # GPIO引脚配置 (适用于全志H618平台)
        self.button_pins = [12, 13]  # PG12和PG13用于按钮控制
        self.led_pins = [16, 17, 18, 19]  # PG16,PG17,PG18,PG19用于LED指示灯
        
        # 数据采集配置
        self.data_update_interval = 3000  # 数据更新间隔(毫秒)
        self.history_data_limit = 100  # 历史数据最大数量
        
        # 数据库配置
        self.database_path = os.getenv('DATABASE_PATH', 'qiuyue.db')
        
    def is_development(self):
        """
        检查是否为开发环境
        
        Returns:
            bool: True表示开发环境，False表示生产环境
        """
        return self.environment == 'development'
        
    def is_production(self):
        """
        检查是否为生产环境
        
        Returns:
            bool: True表示生产环境，False表示开发环境
        """
        return self.environment == 'production'


# 全局配置实例
config = Config()