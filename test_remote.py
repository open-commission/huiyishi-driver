#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试遥控器配置文件
"""

from remote_config import REMOTE_KEYS, PAGE_MAPPING, OPERATION_MAPPING, DEFAULT_PAGE_ORDER, REMOTE_CONFIG

def test_remote_config():
    """
    测试遥控器配置
    """
    print("=== 遥控器配置测试 ===")
    
    print("\n1. 遥控器按键码:")
    for key, value in list(REMOTE_KEYS.items())[:10]:  # 显示前10个
        print(f"  {key}: {value}")
    
    print(f"\n  ... 总共 {len(REMOTE_KEYS)} 个按键码")
    
    print("\n2. 页面映射:")
    for key, value in PAGE_MAPPING.items():
        print(f"  {key}: {value}")
    
    print(f"\n  总共 {len(PAGE_MAPPING)} 个页面映射")
    
    print("\n3. 操作映射 (会议室仪表盘):")
    if 'meeting_dashboard' in OPERATION_MAPPING:
        for op_key, op_value in OPERATION_MAPPING['meeting_dashboard'].items():
            print(f"  {op_key}: {op_value}")
    
    print("\n4. 默认页面顺序:")
    for i, page in enumerate(DEFAULT_PAGE_ORDER):
        print(f"  {i+1}. {page}")
    
    print(f"\n5. 遥控器配置:")
    for key, value in REMOTE_CONFIG.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    test_remote_config()