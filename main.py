from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

from core.query import query_server, SERVER_LIST

@register("Starbound-helper", "Sanka", "-", "0.1.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
    
    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("helloworld")
    async def helloworld(self, event: AstrMessageEvent):
        """这是一个 hello world 指令""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        logger.info(message_chain)
        yield event.plain_result(f"Hello, {user_name}, 你发了 {message_str}!") # 发送一条纯文本消息

    @filter.command("serverquery")
    async def serverquery(self, event: AstrMessageEvent):
        """查询 Starbound 服务器状态"""
        results = []
        for server in SERVER_LIST:
            ip = server["ip"]
            port = server["port"]
            result = query_server(ip, port)
            # if "error" in result:
            #     results.append(f"查询 {ip}:{port} 失败: {result['error']}")
            # else:
            #     results.append(f"{ip}:{port} - 玩家数: {result['players']}, 服务器名称: {result['name']}")
            results.append(str(result))
        yield event.plain_result("\n".join(results))

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
