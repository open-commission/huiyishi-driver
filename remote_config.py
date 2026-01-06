#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
遥控器事件配置文件
定义遥控器按键与系统操作的映射关系
"""

# 遥控器按键码映射
REMOTE_KEYS = {
    # 基本导航按键
    'KEY_OK': 'KEY_OK',          # 确认/选择键
    'KEY_UP': 'KEY_UP',          # 上键
    'KEY_DOWN': 'KEY_DOWN',      # 下键
    'KEY_LEFT': 'KEY_LEFT',      # 左键
    'KEY_RIGHT': 'KEY_RIGHT',    # 右键
    'KEY_HOME': 'KEY_HOME',      # 首页键
    'KEY_BACK': 'KEY_BACK',      # 返回键
    'KEY_MENU': 'KEY_MENU',      # 菜单键
    
    # 数字按键
    'KEY_0': 'KEY_0',
    'KEY_1': 'KEY_1',
    'KEY_2': 'KEY_2',
    'KEY_3': 'KEY_3',
    'KEY_4': 'KEY_4',
    'KEY_5': 'KEY_5',
    'KEY_6': 'KEY_6',
    'KEY_7': 'KEY_7',
    'KEY_8': 'KEY_8',
    'KEY_9': 'KEY_9',
    
    # 功能按键
    'KEY_POWER': 'KEY_POWER',    # 电源键
    'KEY_MUTE': 'KEY_MUTE',      # 静音键
    'KEY_VOLUMEUP': 'KEY_VOLUMEUP',    # 音量+
    'KEY_VOLUMEDOWN': 'KEY_VOLUMEDOWN', # 音量-
    'KEY_CHANNELUP': 'KEY_CHANNELUP',   # 频道+
    'KEY_CHANNELDOWN': 'KEY_CHANNELDOWN', # 频道-
    
    # 其他常用按键
    'KEY_EXIT': 'KEY_EXIT',      # 退出键
    'KEY_INFO': 'KEY_INFO',      # 信息键
    'KEY_GUIDE': 'KEY_GUIDE',    # 指南键
    'KEY_RED': 'KEY_RED',        # 红色键
    'KEY_GREEN': 'KEY_GREEN',    # 绿色键
    'KEY_YELLOW': 'KEY_YELLOW',  # 黄色键
    'KEY_BLUE': 'KEY_BLUE',      # 蓝色键
}

# 页面切换映射 - 每个页面对应一个遥控器按键
PAGE_MAPPING = {
    # 会议室从机相关页面
    'KEY_1': 'meeting_dashboard',      # 会议室从机仪表盘
    'KEY_2': 'meeting_monitor',        # 会议室从机环境监测
    'KEY_3': 'meeting_history',        # 会议室从机历史数据
    'KEY_4': 'meeting_control',        # 会议室控制
    
    # 现场从机相关页面
    'KEY_5': 'field_dashboard',        # 现场从机仪表盘
    'KEY_6': 'field_monitor',          # 现场从机环境监测
    'KEY_7': 'field_history',          # 现场从机历史数据
    'KEY_8': 'device_control',         # 设备控制
    
    # 通用页面
    'KEY_9': 'alarm_config',           # 报警配置
    'KEY_0': 'alarm_monitor',          # 报警监控
    'KEY_HOME': 'main_dashboard',      # 主仪表盘
    'KEY_BACK': 'previous_page',       # 返回上一页
    'KEY_MENU': 'menu',                # 菜单
    'KEY_EXIT': 'exit_app',            # 退出应用
}

# 操作映射 - 定义按键对应的具体操作
OPERATION_MAPPING = {
    # 会议室从机仪表盘操作
    'meeting_dashboard': {
        'KEY_UP': 'scroll_up',
        'KEY_DOWN': 'scroll_down',
        'KEY_LEFT': 'prev_widget',
        'KEY_RIGHT': 'next_widget',
        'KEY_OK': 'select_widget',
    },
    
    # 会议室环境监测操作
    'meeting_monitor': {
        'KEY_UP': 'scroll_up',
        'KEY_DOWN': 'scroll_down',
        'KEY_LEFT': 'prev_chart',
        'KEY_RIGHT': 'next_chart',
        'KEY_OK': 'refresh_data',
    },
    
    # 历史数据显示操作
    'meeting_history': {
        'KEY_UP': 'scroll_up',
        'KEY_DOWN': 'scroll_down',
        'KEY_LEFT': 'prev_page',
        'KEY_RIGHT': 'next_page',
        'KEY_OK': 'refresh_data',
    },
    
    # 会议室控制操作
    'meeting_control': {
        'KEY_UP': 'scroll_up',
        'KEY_DOWN': 'scroll_down',
        'KEY_LEFT': 'prev_control',
        'KEY_RIGHT': 'next_control',
        'KEY_OK': 'toggle_control',
    },
    
    # 现场从机仪表盘操作
    'field_dashboard': {
        'KEY_UP': 'scroll_up',
        'KEY_DOWN': 'scroll_down',
        'KEY_LEFT': 'prev_widget',
        'KEY_RIGHT': 'next_widget',
        'KEY_OK': 'select_widget',
    },
    
    # 现场从机环境监测操作
    'field_monitor': {
        'KEY_UP': 'scroll_up',
        'KEY_DOWN': 'scroll_down',
        'KEY_LEFT': 'prev_chart',
        'KEY_RIGHT': 'next_chart',
        'KEY_OK': 'refresh_data',
    },
    
    # 现场从机历史数据显示操作
    'field_history': {
        'KEY_UP': 'scroll_up',
        'KEY_DOWN': 'scroll_down',
        'KEY_LEFT': 'prev_page',
        'KEY_RIGHT': 'next_page',
        'KEY_OK': 'refresh_data',
    },
    
    # 设备控制操作
    'device_control': {
        'KEY_UP': 'scroll_up',
        'KEY_DOWN': 'scroll_down',
        'KEY_LEFT': 'prev_control',
        'KEY_RIGHT': 'next_control',
        'KEY_OK': 'toggle_control',
    },
    
    # 报警配置操作
    'alarm_config': {
        'KEY_UP': 'scroll_up',
        'KEY_DOWN': 'scroll_down',
        'KEY_LEFT': 'prev_setting',
        'KEY_RIGHT': 'next_setting',
        'KEY_OK': 'confirm_setting',
    },
    
    # 报警监控操作
    'alarm_monitor': {
        'KEY_UP': 'scroll_up',
        'KEY_DOWN': 'scroll_down',
        'KEY_LEFT': 'prev_alarm',
        'KEY_RIGHT': 'next_alarm',
        'KEY_OK': 'acknowledge_alarm',
    },
    
    # 主仪表盘操作
    'main_dashboard': {
        'KEY_UP': 'scroll_up',
        'KEY_DOWN': 'scroll_down',
        'KEY_LEFT': 'prev_section',
        'KEY_RIGHT': 'next_section',
        'KEY_OK': 'select_section',
    },
    
    # 通用操作
    'general': {
        'KEY_HOME': 'go_home',
        'KEY_BACK': 'go_back',
        'KEY_MENU': 'show_menu',
        'KEY_EXIT': 'exit_application',
    }
}

# 默认页面顺序 - 定义遥控器数字键对应的页面顺序
DEFAULT_PAGE_ORDER = [
    'meeting_dashboard',    # KEY_1 - 会议室从机仪表盘
    'meeting_monitor',      # KEY_2 - 会议室从机环境监测
    'meeting_history',      # KEY_3 - 会议室从机历史数据
    'meeting_control',      # KEY_4 - 会议室控制
    'field_dashboard',      # KEY_5 - 现场从机仪表盘
    'field_monitor',        # KEY_6 - 现场从机环境监测
    'field_history',        # KEY_7 - 现场从机历史数据
    'device_control',       # KEY_8 - 设备控制
    'alarm_config',         # KEY_9 - 报警配置
    'alarm_monitor',        # KEY_0 - 报警监控
]

# 遥控器功能配置
REMOTE_CONFIG = {
    'enable_repeat': True,           # 是否启用按键重复
    'repeat_delay': 500,             # 按键重复延迟(毫秒)
    'repeat_interval': 100,          # 按键重复间隔(毫秒)
    'navigation_timeout': 30000,     # 导航超时时间(毫秒)，超过此时间自动返回主页面
    'double_click_interval': 300,    # 双击间隔时间(毫秒)
}