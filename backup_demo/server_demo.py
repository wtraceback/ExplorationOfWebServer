import socket


HOST = '127.0.0.1'      # 标准的回环地址 (localhost)
PORT = 5000             # 监听的端口 （非系统级的端口：大于 1023)

# socket.AF_INET 表示因特网 IPv4 地址族，SOCK_STREAM 表示使用 TCP 的 socket 类型
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))    # 套接字绑定的 IP 与 端口


s.listen(5)
while True:             # 用一个无限循环来处理请求
    connection, address = s.accept()        # 当有客户端过来连接的时候, s.accept 函数就会返回 2 个值
    print('Connected by {}, ip is {}'.format(connection, address))

    request = connection.recv(1024)         # recv 可以接收客户端发送过来的数据，返回值是一个 bytes 类型
    print('request is {}'.format(request))

    # b'' 表示这是一个 bytes 对象
    response = b'HTTP/1.1 200 OK\r\nContent-Type: text/html;charset=utf-8\r\n\r\n<h1>Hello World!</h1>'

    connection.sendall(response)            # 用 sendall 发送给客户端
    connection.close()                      # 发送完毕后, 关闭本次连接
