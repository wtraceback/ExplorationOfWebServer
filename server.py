import socket

from routes import route_index


def error(code=404):
    """
    根据 code 返回不同的错误响应
    """
    e = {
        404: b'HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n<h1>NOT FOUND</h1>',
    }

    return e.get(code, b'')


def response_for_path(path):
    """
    根据 path 调用相应的处理函数
    没有处理的 path 就返回 错误处理
    """
    r = {
        '/': route_index,
    }

    response = r.get(path, error)

    return response()


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


def run(host='127.0.0.1', port=3000):
    """
    启动服务器
    """
    # 初始化 socket，使用 with 可以保证程序中断的时候正确关闭 socket 释放占用的端口
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))        # 套接字绑定的 IP 与 端口
        print('Server start at', '{}:{}.'.format(host, port))

        # 用一个无限循环来处理请求
        while True:
            s.listen(5)
            connection, address = s.accept()        # 当有客户端过来连接的时候, s.accept 函数就会返回 2 个值
            print('Connected by {}\nip is {}'.format(connection, address))

            # 获取请求的数据
            request = receive_by_request(connection)
            request = request.decode('utf-8')
            print('request is:\n {}'.format(request))

            try:
                path = request.split()[1]
                # 用 response_for_path 函数来得到 path 对应的响应内容
                response = response_for_path(path)
                # response = b'HTTP/1.1 200 OK\r\nContent-Type: text/html;charset=utf-8\r\n\r\n<h1>Hello World!</h1>'
                connection.sendall(response)            # 用 sendall 发送给客户端
            except Exception as e:
                print('error', e)

            connection.close()                          # 发送完毕后, 关闭本次连接


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
