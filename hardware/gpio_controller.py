#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GPIO控制器
用于读取GPIO状态并控制页面切换
支持全志H618平台
"""

import time
import os
from PyQt6.QtCore import QTimer, QObject, pyqtSignal
from config import config


class GPIOController(QObject):
    """
    GPIO控制器类
    用于读取GPIO引脚状态并发出页面切换信号
    """
    # 定义信号，用于通知页面切换
    page_changed = pyqtSignal(int)  # 页面索引从0开始
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 仅在生产环境中初始化GPIO
        if not config.is_production():
            print("开发环境，GPIO功能已禁用")
            self.gpio_initialized = False
            return
        
        # GPIO引脚配置 (适用于全志H618平台)
        self.button_pins = config.button_pins  # PG12和PG13用于按钮控制
        self.led_pins = config.led_pins  # PG16,PG17,PG18,PG19用于LED指示灯
        
        # 状态变量
        self.current_page = 0
        self.max_pages = 0
        self.last_button_states = [1, 1]  # 默认高电平（假设使用上拉电阻）
        self.debounce_time = 0.2  # 消抖时间（秒）
        self.last_button_press = [0, 0]  # 上次按键时间
        
        # 初始化GPIO
        self.gpio_initialized = self.init_gpio()
        
        # 初始化定时器用于轮询GPIO状态
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_gpio_states)
        if self.gpio_initialized:
            self.timer.start(100)  # 每100ms检查一次
    
    def init_gpio(self):
        """
        初始化GPIO引脚
        
        Returns:
            bool: 初始化是否成功
        """
        # 仅在生产环境中初始化GPIO
        if not config.is_production():
            return False
            
        try:
            # 尝试使用sysfs接口初始化GPIO
            for pin in self.button_pins + self.led_pins:
                if not self.setup_gpio_pin(pin):
                    return False
                    
            # 设置按钮引脚为输入模式
            for pin in self.button_pins:
                self.set_gpio_direction(pin, "in")
            
            # 设置LED引脚为输出模式
            for pin in self.led_pins:
                self.set_gpio_direction(pin, "out")
                self.set_gpio_value(pin, 0)  # 默认关闭LED
                
            print("GPIO初始化成功")
            return True
        except Exception as e:
            print(f"GPIO初始化失败: {e}")
            print("使用模拟模式")
            return False
    
    def setup_gpio_pin(self, pin):
        """
        设置GPIO引脚
        
        Args:
            pin: GPIO引脚编号
            
        Returns:
            bool: 设置是否成功
        """
        try:
            gpio_path = f"/sys/class/gpio/gpio{pin}"
            
            # 检查GPIO是否已经导出
            if not os.path.exists(gpio_path):
                # 导出GPIO
                with open("/sys/class/gpio/export", "w") as f:
                    f.write(str(pin))
                
                # 等待系统创建GPIO目录
                time.sleep(0.1)
                
            return os.path.exists(gpio_path)
        except Exception as e:
            print(f"设置GPIO {pin} 失败: {e}")
            return False
    
    def set_gpio_direction(self, pin, direction):
        """
        设置GPIO方向
        
        Args:
            pin: GPIO引脚编号
            direction: 方向 ("in" 或 "out")
        """
        try:
            direction_path = f"/sys/class/gpio/gpio{pin}/direction"
            with open(direction_path, "w") as f:
                f.write(direction)
        except Exception as e:
            print(f"设置GPIO {pin} 方向失败: {e}")
    
    def set_gpio_value(self, pin, value):
        """
        设置GPIO值
        
        Args:
            pin: GPIO引脚编号
            value: 值 (0 或 1)
        """
        try:
            value_path = f"/sys/class/gpio/gpio{pin}/value"
            with open(value_path, "w") as f:
                f.write(str(value))
        except Exception as e:
            print(f"设置GPIO {pin} 值失败: {e}")
    
    def get_gpio_value(self, pin):
        """
        获取GPIO值
        
        Args:
            pin: GPIO引脚编号
            
        Returns:
            int: GPIO值 (0 或 1)
        """
        try:
            value_path = f"/sys/class/gpio/gpio{pin}/value"
            with open(value_path, "r") as f:
                return int(f.read().strip())
        except Exception as e:
            print(f"读取GPIO {pin} 值失败: {e}")
            return 1  # 默认返回高电平
    
    def check_gpio_states(self):
        """
        检查GPIO状态并处理按钮按下事件
        """
        if not self.gpio_initialized:
            return
            
        try:
            # 读取按钮状态
            button_states = []
            for pin in self.button_pins:
                button_states.append(self.get_gpio_value(pin))
            
            current_time = time.time()
            
            # 检查第一个按钮（PG12）- 上一个页面
            if button_states[0] == 0 and self.last_button_states[0] == 1:  # 按下事件
                if current_time - self.last_button_press[0] > self.debounce_time:
                    self.switch_to_previous_page()
                    self.last_button_press[0] = current_time
            
            # 检查第二个按钮（PG13）- 下一个页面
            if button_states[1] == 0 and self.last_button_states[1] == 1:  # 按下事件
                if current_time - self.last_button_press[1] > self.debounce_time:
                    self.switch_to_next_page()
                    self.last_button_press[1] = current_time
            
            # 更新按钮状态
            self.last_button_states = button_states
            
            # 更新LED指示灯
            self.update_led_indicators()
            
        except Exception as e:
            print(f"检查GPIO状态时出错: {e}")
    
    def switch_to_next_page(self):
        """
        切换到下一个页面
        """
        if self.max_pages > 0:
            self.current_page = (self.current_page + 1) % self.max_pages
            self.page_changed.emit(self.current_page)
    
    def switch_to_previous_page(self):
        """
        切换到上一个页面
        """
        if self.max_pages > 0:
            self.current_page = (self.current_page - 1) % self.max_pages
            self.page_changed.emit(self.current_page)
    
    def set_max_pages(self, max_pages):
        """
        设置最大页面数
        
        Args:
            max_pages: 最大页面数
        """
        self.max_pages = max_pages
    
    def set_current_page(self, page_index):
        """
        设置当前页面
        
        Args:
            page_index: 页面索引
        """
        if 0 <= page_index < self.max_pages:
            self.current_page = page_index
            self.update_led_indicators()
    
    def update_led_indicators(self):
        """
        更新LED指示灯状态
        """
        if not self.gpio_initialized:
            return
            
        try:
            # 简单的LED指示方案：
            # 使用前4个LED表示页面状态，当前页面对应的LED亮起
            for i, pin in enumerate(self.led_pins):
                if i < self.max_pages and i == self.current_page:
                    self.set_gpio_value(pin, 1)
                else:
                    self.set_gpio_value(pin, 0)
        except Exception as e:
            print(f"更新LED指示灯时出错: {e}")
    
    def cleanup(self):
        """
        清理GPIO资源
        """
        if self.gpio_initialized:
            try:
                # 关闭所有LED
                for pin in self.led_pins:
                    self.set_gpio_value(pin, 0)
                
                print("GPIO资源已清理")
            except Exception as e:
                print(f"清理GPIO资源时出错: {e}")


# 模拟测试代码
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
    from PyQt6.QtCore import Qt
    import sys
    
    class TestWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("GPIO控制器测试")
            self.setGeometry(100, 100, 400, 300)
            
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            layout = QVBoxLayout(central_widget)
            
            self.label = QLabel("当前页面: 0")
            self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(self.label)
            
            self.gpio_controller = GPIOController()
            self.gpio_controller.set_max_pages(4)
            self.gpio_controller.page_changed.connect(self.on_page_changed)
        
        def on_page_changed(self, page_index):
            self.label.setText(f"当前页面: {page_index}")
        
        def closeEvent(self, event):
            self.gpio_controller.cleanup()
            event.accept()
    
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())