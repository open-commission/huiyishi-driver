#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CoAP客户端基本示例

此模块演示了如何使用aiocoap库创建一个基本的CoAP客户端。
包含基本的GET请求功能，适合初学者学习和测试。
展示了如何在GET请求中传递参数以及如何使用观察（订阅）功能。
"""

import asyncio
import logging
from typing import Optional
import urllib.parse
import aiocoap
from aiocoap import Context, Message, Code


class BasicCoapClient:
    """
    基本CoAP客户端类
    
    实现了CoAP客户端的基本功能，包括连接管理、请求发送和响应处理
    """

    def __init__(self):
        """
        初始化CoAP客户端
        """
        # 设置日志记录器
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # CoAP上下文
        self.context: Optional[Context] = None

        # 存储观察请求的任务
        self.observation_tasks = []

    async def initialize(self):
        """
        初始化CoAP客户端上下文
        """
        self.context = await Context.create_client_context()
        self.logger.info("CoAP客户端上下文已创建")

    async def shutdown(self):
        """
        关闭CoAP客户端并清理资源
        """
        # 取消所有观察任务
        for task in self.observation_tasks:
            task.cancel()

        if self.context:
            await self.context.shutdown()
            self.logger.info("CoAP客户端已关闭")

    async def get(self, uri: str) -> Optional[str]:
        """
        发送GET请求到指定URI并返回响应数据
        
        Args:
            uri: 目标URI
            
        Returns:
            Optional[str]: 响应数据字符串，如果失败则返回None
        """
        try:
            # 创建GET请求消息
            request = Message(code=Code.GET, uri=uri)

            self.logger.info(f"发送GET请求到: {uri}")

            # 发送请求并等待响应
            response = await self.context.request(request).response

            # 检查响应码
            if response.code.is_successful():
                # 解码并返回响应数据
                payload_str = response.payload.decode('utf-8', errors='ignore')
                self.logger.info(f"成功接收到响应: {response.code}")
                print(f"响应数据: {payload_str}")
                return payload_str
            else:
                self.logger.error(f"请求失败: {response.code} - {response.code.name}")
                return None

        except Exception as e:
            self.logger.error(f"发送请求失败: {e}")
            return None

    async def get_with_params(self, base_uri: str, params: dict) -> Optional[str]:
        """
        发送带参数的GET请求到指定URI并返回响应数据
        
        Args:
            base_uri: 目标URI基础部分
            params: 参数字典
            
        Returns:
            Optional[str]: 响应数据字符串，如果失败则返回None
        """
        try:
            # 将参数字典转换为查询字符串
            query_string = urllib.parse.urlencode(params)
            full_uri = f"{base_uri}?{query_string}"

            # 创建GET请求消息
            request = Message(code=Code.GET, uri=full_uri)

            self.logger.info(f"发送带参数的GET请求到: {full_uri}")

            # 发送请求并等待响应
            response = await self.context.request(request).response

            # 检查响应码
            if response.code.is_successful():
                # 解码并返回响应数据
                payload_str = response.payload.decode('utf-8', errors='ignore')
                self.logger.info(f"成功接收到响应: {response.code}")
                print(f"响应数据: {payload_str}")
                return payload_str
            else:
                self.logger.error(f"请求失败: {response.code} - {response.code.name}")
                return None

        except Exception as e:
            self.logger.error(f"发送请求失败: {e}")
            return None

    async def observe_resource(self, uri: str, callback=None):
        """
        观察（订阅）指定URI的资源变化
        
        Args:
            uri: 要观察的URI
            callback: 可选的回调函数，当收到更新时调用
        """
        try:
            # 创建观察请求消息
            request = Message(code=Code.GET, uri=uri)
            # 设置Observe选项，值为0表示开始观察
            request.opt.observe = 0
            
            self.logger.info(f"开始观察资源: {uri}")
            print(f"正在观察资源: {uri}，等待更新...")
            
            # 发起观察请求
            observation = self.context.request(request).observation
            self.observation_tasks.append(observation)
            
            # 异步处理观察响应
            async for response in observation:
                # 检查响应码
                if response.code.is_successful():
                    payload_str = response.payload.decode('utf-8', errors='ignore')
                    self.logger.info(f"收到资源更新: {response.code}")
                    print(f"【资源更新】时间戳: {response.opt.observe}, 数据: {payload_str}")
                    
                    # 如果提供了回调函数，则调用它（区分协程和普通函数）
                    if callback:
                        if asyncio.iscoroutinefunction(callback):
                            await callback(response)
                        else:
                            callback(response)
                else:
                    self.logger.error(f"观察请求失败: {response.code} - {response.code.name}")
                    break
        
        except Exception as e:
            self.logger.error(f"观察资源时发生错误: {e}")

    async def stop_observing_all(self):
        """
        停止所有观察任务
        """
        for task in self.observation_tasks:
            if hasattr(task, 'cancel') and not task.cancelled:
                task.cancel()
        self.observation_tasks.clear()
        self.logger.info("已停止所有观察任务")

    async def post(self, uri: str, data: str) -> Optional[str]:
        """
        发送POST请求到指定URI
        
        Args:
            uri: 目标URI
            data: 要发送的数据
            
        Returns:
            Optional[str]: 响应数据字符串，如果失败则返回None
        """
        try:
            # 创建POST请求消息
            request = Message(code=Code.POST, uri=uri, payload=data.encode('utf-8'))

            self.logger.info(f"发送POST请求到: {uri}，数据: {data}")

            # 发送请求并等待响应
            response = await self.context.request(request).response

            # 检查响应码
            if response.code.is_successful():
                # 解码并返回响应数据
                payload_str = response.payload.decode('utf-8', errors='ignore')
                self.logger.info(f"成功接收到响应: {response.code}")
                print(f"响应数据: {payload_str}")
                return payload_str
            else:
                self.logger.error(f"请求失败: {response.code} - {response.code.name}")
                return None

        except Exception as e:
            self.logger.error(f"发送请求失败: {e}")
            return None

    async def put(self, uri: str, data: str) -> Optional[str]:
        """
        发送PUT请求到指定URI
        
        Args:
            uri: 目标URI
            data: 要发送的数据
            
        Returns:
            Optional[str]: 响应数据字符串，如果失败则返回None
        """
        try:
            # 创建PUT请求消息
            request = Message(code=Code.PUT, uri=uri, payload=data.encode('utf-8'))

            self.logger.info(f"发送PUT请求到: {uri}，数据: {data}")

            # 发送请求并等待响应
            response = await self.context.request(request).response

            # 检查响应码
            if response.code.is_successful():
                # 解码并返回响应数据
                payload_str = response.payload.decode('utf-8', errors='ignore')
                self.logger.info(f"成功接收到响应: {response.code}")
                print(f"响应数据: {payload_str}")
                return payload_str
            else:
                self.logger.error(f"请求失败: {response.code} - {response.code.name}")
                return None

        except Exception as e:
            self.logger.error(f"发送PUT请求失败: {e}")
            return None

    async def delete(self, uri: str) -> Optional[str]:
        """
        发送DELETE请求到指定URI
        
        Args:
            uri: 目标URI
            
        Returns:
            Optional[str]: 响应数据字符串，如果失败则返回None
        """
        try:
            # 创建DELETE请求消息
            request = Message(code=Code.DELETE, uri=uri)

            self.logger.info(f"发送DELETE请求到: {uri}")

            # 发送请求并等待响应
            response = await self.context.request(request).response

            # 检查响应码
            if response.code.is_successful():
                # 解码并返回响应数据
                payload_str = response.payload.decode('utf-8', errors='ignore')
                self.logger.info(f"成功接收到响应: {response.code}")
                print(f"响应数据: {payload_str}")
                return payload_str
            else:
                self.logger.error(f"请求失败: {response.code} - {response.code.name}")
                return None

        except Exception as e:
            self.logger.error(f"发送DELETE请求失败: {e}")
            return None


def resource_update_callback(response):
    """
    资源更新的回调函数示例
    """
    print(f"  → 回调函数被调用，处理更新数据: {response.payload.decode('utf-8', errors='ignore')}")


async def main():
    """
    主函数 - 演示基本CoAP客户端的使用
    """
    # 设置日志记录
    logging.basicConfig(level=logging.INFO)

    # 创建CoAP客户端实例
    client = BasicCoapClient()

    try:
        # 初始化客户端
        await client.initialize()

        # 测试CoAP服务器 - 使用公共测试服务器
        server_uri = "coap://192.168.1.100:5683/Espressif"

        print("=== 基本CoAP客户端测试 ===")

        # # 示例1: 发送带参数的GET请求
        # print("\n1. 发送带参数的GET请求")
        # params = {"name": "test", "value": "123"}
        # response = await client.get_with_params(f"{server_uri}", params)
        # if response:
        #     print(f"带参数GET响应: {response}")
        # else:
        #     print("带参数GET请求失败或服务器不支持参数")

        # # 示例2: 发送POST请求（演示POST功能）
        # print("\n2. 发送POST请求")
        # response = await client.post(f"{server_uri}", "test data")
        # if response:
        #     print(f"POST响应: {response}")
        # else:
        #     print("POST请求失败或资源不支持POST")

        # # 示例3: 发送PUT请求（演示PUT功能）
        # print("\n3. 发送PUT请求")
        # response = await client.put(f"{server_uri}", "updated data")
        # if response:
        #     print(f"PUT响应: {response}")
        # else:
        #     print("PUT请求失败或资源不支持PUT")

        # # 示例4: 发送DELETE请求（演示DELETE功能）
        # print("\n4. 发送DELETE请求")
        # response = await client.delete(f"{server_uri}")
        # if response:
        #     print(f"DELETE响应: {response}")
        # else:
        #     print("DELETE请求失败或资源不支持DELETE")

        # 示例5: 监听资源变化（演示observe功能）
        print("\n5. 开始监听资源变化")
        print("注意：监听功能将持续运行，接收资源更新通知...")
        try:
            # 启动监听任务并保存引用
            observe_task = asyncio.create_task(client.observe_resource(f"{server_uri}", resource_update_callback))
            
            # 等待一段时间让监听建立
            await asyncio.sleep(2)
            
            # 等待一段时间以接收观察更新
            await asyncio.sleep(10)
            
            # 停止监听
            await client.stop_observing_all()
            print("已停止监听资源变化")
        except Exception as e:
            print(f"监听过程中发生错误: {e}")
            await client.stop_observing_all()
        
        print("\n=== 测试完成 ===")
        
    except Exception as e:
        print(f"测试过程中发生错误: {e}")
    finally:
        # 关闭客户端
        await client.shutdown()


# 兼容旧版本Python的运行方式
if __name__ == "__main__":
    asyncio.run(main())
