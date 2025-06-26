import re;

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