import re;
import requests_unixsocket

from gamedig import query
from socket import gethostbyname

def query_server(ip: str, port: int):
    try:
        return query('starbound', gethostbyname(ip), port)
    except Exception as e:
        return {'error': str(e)}
    
def strip_escape_codes(text: str) -> str:
    """
        去除文本中的转义代码
        转移码规定为 ^xxx; 格式
    """
    return re.sub(r'\^.*?;', '', text).strip()

def reboot_container(container_name: str):
    """
        重启 Docker 容器
        需要安装 requests_unixsocket 库
    """
    try:
        session = requests_unixsocket.Session()
        r = session.post('http+unix://%2Fvar%2Frun%2Fdocker.sock/containers/{}/restart'.format(container_name))
        return {'status_code': r.status_code, 'response': r.text}
    except Exception as e:
        return {'error': str(e)}