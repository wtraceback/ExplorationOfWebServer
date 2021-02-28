import socket


HOST = '127.0.0.1'      # 服务器的主机名或者 IP 地址
PORT = 5000             # 服务器使用的端口


# socket.AF_INET 表示因特网 IPv4 地址族，SOCK_STREAM 表示使用 TCP 的 socket 类型
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))     # 要连接的 IP 与 端口

s.sendall(b'Client say: Hello World')

# 接受服务器的响应数据，如果服务器返回的数据中超过 1024 的部分你就得不到了
response = s.recv(1024)
print('响应 is {}'.format(response))

s.close()       # 关闭连接
