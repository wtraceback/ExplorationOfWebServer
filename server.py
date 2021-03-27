import socket
import urllib.parse
import _thread

from routes.routes_index import route_dict
from routes.routes_auth import route_dict as auth_routes
from routes.routes_static import route_dict as static_routes
from routes.routes_todo import route_dict as todo_routes
from routes.routes_admin import route_dict as admin_routes
from routes.routes_weibo import route_dict as weibo_routes
from routes.routes_api_todo import route_dict as api_todo_routes
from routes.api_todo import route_dict as api_todo
from utils import (
    log,
    error,
)


# 定义一个 class 用于保存请求的数据
class Request(object):
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''
        self.headers = {}
        self.cookies = {}

    def set_cookies(self):
        """
        从 self.headers 的 cookie 字段中获取 cookie 的值并生成字典赋值给 self.cookie
        Cookie: PSTM=1612061500; BD_UPN=12314353; ispeed_lsm=2; delPer=0
        """
        cookies = self.headers.get('Cookie', '')
        cs = cookies.split('; ')
        for c in cs:
            if '=' in c:
                k, v = c.split('=', 1)
                self.cookies[k] = v

    def set_headers(self, header):
        """
        根据请求的 headers 将其解析出来
        [
            'Connection: keep-alive',
            'Pragma: no-cache',
            'Cache-Control: no-cache'
        ]
        """
        lines = header
        for line in lines:
            k, v = line.split(': ', 1)
            self.headers[k] = v

        self.set_cookies()

    def form(self):
        """
        form 函数用于把 post 请求的 body 解析为一个字典并返回
        post 请求的 body 为
            firstname=Mickey&lastname=Mouse
            firstname=Micke+y&lastname=%26Mouse

        #解决地址栏中 中文编码问题
            typename = urllib.parse.quote(index)
        #解码
            retypename = urllib.parse.unquote(typename)
        """
        args = self.body.split('&')
        f = {}
        for arg in args:
            k, v = arg.split('=')
            f[k] = urllib.parse.unquote(v)

        return f

    def json(self):
        """
        把 body 中的 json 格式字符串解析成 dict 或者 list 并返回
        """
        import json
        return json.loads(self.body)


def parsed_path(path):
    """
    根据 path 将 路径 和 参数 解析出来
    """
    i = path.find('?')
    if i == -1:
        return path, {}
    else:
        path, query_string = path.split('?', 1)
        args = query_string.split('&')
        query = {}
        for arg in args:
            k, v = arg.split('=')
            query[k] = v

        return path, query


def response_for_path(path, request):
    """
    根据 path 调用相应的处理函数
    没有处理的 path 就返回 错误处理
    """
    path, query = parsed_path(path)
    request.path = path
    request.query = query
    log('path is {} and query is {}'.format(path, query))

    r = {
        # '/': route_index,
        # '/static': static
    }

    # 往 r 中添加 新的路由
    r.update(route_dict)
    r.update(auth_routes)
    r.update(static_routes)
    r.update(todo_routes)
    r.update(admin_routes)
    r.update(weibo_routes)
    r.update(api_todo_routes)
    r.update(api_todo)

    response = r.get(path, error)

    return response(request)


def receive_by_request(conn):
    """
    参数是一个 socket 示例
    返回这个 socket 读取的所有请求的数据
    """
    req = b''
    buffer_size = 1024
    while True:
        # recv 可以接收客户端发送过来的数据，返回值是一个 bytes 类型
        r = conn.recv(buffer_size)
        req += r
        if len(r) < buffer_size:
            break

    return req


def process_request(connection):
    """
    处理每一个连接的 request
    """
    # 获取请求的数据
    r = receive_by_request(connection)
    r = r.decode('utf-8')
    log('request is:\n {}'.format(r))

    # Chrome 浏览器会发送空请求导致 split 得到空 list， 所以需要判断一下，防止程序崩溃
    if len(r.split()) < 2:
        connection.close()
        return None

    # 创建一个新的 request 并设置
    request = Request()

    # 通过切分获取请求数据中的相关信息
    req_line = r.split()
    path = req_line[1]
    request.method = req_line[0]
    h_b_line = r.split('\r\n\r\n', 1)
    request.set_headers(h_b_line[0].split('\r\n')[1:])
    request.body = h_b_line[1]

    # 用 response_for_path 函数来得到 path 对应的响应内容
    response = response_for_path(path, request)
    # response = b'HTTP/1.1 200 OK\r\nContent-Type: text/html;charset=utf-8\r\n\r\n<h1>Hello World!</h1>'
    connection.sendall(response)            # 用 sendall 发送给客户端

    connection.close()                          # 发送完毕后, 关闭本次连接
    print('线程关闭')


def run(host='127.0.0.1', port=3000):
    """
    启动服务器
    """
    # 初始化 socket，使用 with 可以保证程序中断的时候正确关闭 socket 释放占用的端口
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))        # 套接字绑定的 IP 与 端口
        print('Server start at', '{}:{}.'.format(host, port))

        s.listen(5)
        # 用一个无限循环来处理请求
        while True:
            connection, address = s.accept()        # 当有客户端过来连接的时候, s.accept 函数就会返回 2 个值
            print('New client connection {}'.format(address))
            log('Connected by {}\nip is {}'.format(connection, address))
            print('使用多线程处理请求', address)

            # 开一个新的线程来处理请求, 第二个参数是传给新函数的参数列表, 必须是 tuple
            _thread.start_new_thread(process_request, (connection,))


def main():
    """
    程序入口
    """
    # 生成配置并且运行程序
    config = dict(
        host='127.0.0.1',
        port=3000,
    )

    run(**config)


if __name__ == '__main__':
    main()
