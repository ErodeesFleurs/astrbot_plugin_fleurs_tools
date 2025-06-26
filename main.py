from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.core.config.astrbot_config import AstrBotConfig

from .core.utils import query_server, strip_escape_codes

@register("Starbound-helper", "Sanka", "-", "0.1.0")
class StarHelperPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    @filter.command("serverquery")
    async def serverquery(self, event: AstrMessageEvent):
        """查询 Starbound 服务器状态"""
        results = []
        server_list = self.config.get("server_list", [])
        for server in server_list:
            ip_port = server.split(":")
            ip = ip_port[0]
            port = int(ip_port[1]) if len(ip_port) > 1 else 21025
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
        logger.info(f"查询结果: {results}")
        yield event.plain_result("\n".join(results))

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
