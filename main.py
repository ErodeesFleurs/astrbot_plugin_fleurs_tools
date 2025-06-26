from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

from .core.utils import query_server, strip_escape_codes, SERVER_LIST

@register("Starbound-helper", "Sanka", "-", "0.1.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    @filter.command("serverquery")
    async def serverquery(self, event: AstrMessageEvent):
        """查询 Starbound 服务器状态"""
        results = []
        for server in SERVER_LIST:
            ip = server["ip"]
            port = server["port"]
            result = query_server(ip, port)
            if "error" in result:
                results.append(f"IP: {ip}:{port}\n\t查询失败: {result['error']}")
            else:
                player_res = result.get('players')
                player_list = []
                if isinstance(player_res, list):
                    for player in player_res:
                        player_list.append(strip_escape_codes(player['name']))
                results.append(f"IP: {ip}:{port}\n\t- 玩家数: {result['players_online']}\n\t- 玩家列表 [{', '.join(player_list)}]")
        yield event.plain_result("\n".join(results))

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
