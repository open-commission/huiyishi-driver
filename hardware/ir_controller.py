#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
红外控制器
用于监听红外事件并处理红外按键
"""

import datetime
import threading
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from config import config


class IRController(QObject):
    """
    红外控制器类
    用于监听红外事件并发出相应信号
    """
    # 定义信号
    ir_key_pressed = pyqtSignal(str)  # 红外按键按下信号，参数为按键码
    ir_key_released = pyqtSignal(str)  # 红外按键释放信号，参数为按键码
    ir_event_logged = pyqtSignal(str)  # 红外事件日志信号，参数为日志信息

    def __init__(self, parent=None, device_path='/dev/input/event0'):
        super().__init__(parent)
        
        # 设备路径
        self.device_path = device_path
        
        # 线程控制
        self.ir_thread = None
        self.ir_running = False
        
        # 仅在生产环境中启用红外监听
        if not config.is_production():
            print("开发环境，红外功能已禁用")
            self.ir_enabled = False
        else:
            self.ir_enabled = True
            # 检查是否有evdev库
            try:
                import evdev
                from evdev import InputDevice, categorize, ecodes
                self.evdev_available = True
            except ImportError:
                print("evdev库未安装，红外功能不可用")
                self.evdev_available = False
                self.ir_enabled = False

    def start_ir_monitoring(self):
        """
        开始红外监控
        """
        if not self.ir_enabled or not self.evdev_available:
            print("红外监控未启用或evdev库不可用")
            return

        if self.ir_running:
            print("红外监控已在运行中")
            return

        # 创建并启动红外监听线程
        self.ir_running = True
        self.ir_thread = threading.Thread(target=self._ir_monitor_loop, daemon=True)
        self.ir_thread.start()
        print(f"红外监控已启动，设备: {self.device_path}")

    def stop_ir_monitoring(self):
        """
        停止红外监控
        """
        self.ir_running = False
        if self.ir_thread and self.ir_thread.is_alive():
            self.ir_thread.join(timeout=1)
        print("红外监控已停止")

    def _ir_monitor_loop(self):
        """
        红外监控循环
        """
        if not self.evdev_available:
            return

        import evdev
        from evdev import InputDevice, categorize, ecodes

        try:
            # 尝试打开设备
            dev = InputDevice(self.device_path)
            self.ir_event_logged.emit(f"监听红外事件: {dev.name} ({self.device_path})")
            
            for event in dev.read_loop():
                if not self.ir_running:
                    break
                    
                if event.type == ecodes.EV_KEY:  # KEY 事件
                    key_event = categorize(event)
                    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    if key_event.keystate == key_event.key_down:
                        self.ir_key_pressed.emit(key_event.keycode)
                        log_msg = f"[{timestamp}] 按下: {key_event.keycode}"
                        self.ir_event_logged.emit(log_msg)
                    elif key_event.keystate == key_event.key_up:
                        self.ir_key_released.emit(key_event.keycode)
                        log_msg = f"[{timestamp}] 松开: {key_event.keycode}"
                        self.ir_event_logged.emit(log_msg)
                elif event.type == ecodes.EV_MSC:  # MISC 事件
                    log_msg = f"MISC事件: {event}"
                    self.ir_event_logged.emit(log_msg)
                    
        except FileNotFoundError:
            error_msg = f"无法找到红外设备: {self.device_path}"
            self.ir_event_logged.emit(error_msg)
            print(error_msg)
        except PermissionError:
            error_msg = f"权限不足，无法访问红外设备: {self.device_path}"
            self.ir_event_logged.emit(error_msg)
            print(error_msg)
        except Exception as e:
            error_msg = f"红外监控出错: {str(e)}"
            self.ir_event_logged.emit(error_msg)
            print(error_msg)

    def cleanup(self):
        """
        清理资源
        """
        self.stop_ir_monitoring()