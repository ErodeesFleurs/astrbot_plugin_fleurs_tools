from gamedig import query

SERVER_LIST = [
    {
        "ip": "starbuddy.top",
        "port": 21025
    },
    {
        "ip": "starbound-china.com",
        "port": 21025
    }
]

def query_server(ip: str, port: int):
    try:
        return query('starbound', ip, port)
    except Exception as e:
        return {'error': str(e)}