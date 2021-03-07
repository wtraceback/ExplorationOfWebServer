import socket
import ssl
from bs4 import BeautifulSoup


def parsed_url(url):
    """
    解析 url 返回 (protocol host port path)
    """
    # 检查协议
    protocol = 'http'
    if url[:7] == 'http://':
        u = url.split('://')[1]
    elif url[:8] == 'https://':
        protocol = 'https'
        u = url.split('://')[1]
    else:
        u = url

    # 检查端口
    port_dict = {
        'http': 80,
        'https': 443,
    }
    # 默认端口
    port = port_dict[protocol]

    # 检查路径
    i = u.find('/')
    if i == -1:
        host = u
        path = '/'
    else:
        host = u[:i]
        path = u[i:]

    # 检查主机
    if ':' in host:
        h = host.split(':')
        host = h[0]
        port = int(h[1])

    return protocol, host, port, path


def socket_by_protocol(protocol):
    """
    根据协议返回一个 socket 实例
    """
    if protocol == 'http':
        # 参数 socket.AF_INET 表示是 ipv4 协议
        # 参数 socket.SOCK_STREAM 表示是 tcp 协议
        # 这两个其实是默认值, 所以可以不写
        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s = socket.socket()
    else:
        # HTTPS 协议需要使用 ssl.wrap_socket 包装一下原始的 socket
        s = ssl.wrap_socket(socket.socket())

    return s


def response_by_socket(s):
    """
    参数是一个 socket 实例
    返回这个 socket 读取的所有数据
    """
    response = b''
    buffer_size = 1024
    while True:
        r = s.recv(buffer_size)
        response += r
        if len(r) < buffer_size:
            break

    return response


def parsed_response(r):
    """
    把 response 解析出 状态码 headers body 返回
    状态码是 int
    headers 是 dict
    body 是 str
    """
    # 获取 body
    header, body = r.split('\r\n\r\n', 1)
    h = header.split('\r\n')

    # 获取 int 类型的状态码
    status_code = h[0].split()[1]
    status_code = int(status_code)

    headers = {}
    for line in h[1:]:
        k, v = line.split(': ')
        headers[k] = v

    return status_code, headers, body


def path_with_query(path, query):
    '''
    path 是一个字符串
    query 是一个字典
    返回一个拼接后的 带参数的路径
    '''
    r = path + '?'

    for key, value in query.items():
        r += '{}={}&'.format(key, value)

    return r[:-1]


def get(url, query={}):
    """
    用 GET 请求 url 并返回响应
    """
    # 建立连接 （解析 url、获取 ip、通过 3 次握手建立 tcp 连接）
    protocol, host, port, path = parsed_url(url)
    path = path_with_query(path, query)
    s = socket_by_protocol(protocol)
    s.connect((host, port))

    # 发送请求 （建立连接后，浏览器自动添加请求中必要的 headers，然后发送请求）
    request = 'GET {} HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n'.format(path, host)
    encoding = 'utf-8'
    s.sendall(request.encode(encoding))

    # 获取响应的数据 （获取服务器的响应，然后解析，将数据传递到上层的 jquery）
    response = response_by_socket(s)
    r = response.decode(encoding)

    # 解析响应的数据，如果是重定向，则重新发起请求 （如果是重定向，则自动跳转到重定向的链接）
    status_code, headers, body = parsed_response(r)
    if status_code in [301, 302]:
        url = headers['Location']
        return get(url)

    return status_code, headers, body


def save_to_file(data):
    path = '豆瓣电影Top250.txt'
    with open(path, 'a+', encoding='utf-8') as f:
        print('数据正在保存中...')
        f.write(data)


def extract_html_message(html_doc):
    """
    提取网页中需要的数据
    """
    soup = BeautifulSoup(html_doc, 'html.parser')
    movie_list = soup.select('#content .article li')
    r = ''

    for m in movie_list:
        # 名次
        rank = m.select('.item .pic em')[0].get_text()

        # 电影名
        name = m.select('.item .info .hd .title')[0].get_text()

        # 评分
        score = m.select('.item .bd .rating_num')[0].get_text()

        # 评价的人数
        num_evaluate = m.select('.item .bd .star span:last-child')[0].get_text()

        # 引用语
        quote = m.select('.item .bd .quote .inq')
        if len(quote) != 0:
            quote = quote[0].get_text()
        else:
            quote = ''

        info = 'Top {}\n电影名: {}\n分数: {}\n评价人数: {}\n引用语: {}\n\n'.format(rank, name, score, num_evaluate, quote)
        r += info

    # 提取后面的页数的链接
    a_href = soup.select('.paginator > a')

    return r, a_href


def parse_query_to_dict(query):
    """
    将参数解析为字典
    """
    l = query[1:].split('&')
    r = {}

    for i in l:
        t = i.split('=')
        k = t[0]
        v = t[1]
        r[k] = v

    return r


def main():
    """
    程序入口
    """
    # （浏览器中输入 url）
    url = 'http://movie.douban.com/top250'
    status_code, headers, body = get(url)

    print('status_code is {}'.format(status_code))
    print('headers is {}'.format(headers))
    # print('body is {}'.format(body))

    data, a_href = extract_html_message(body)
    # print('movie info is {}'.format(movie_infos))
    # 写文件
    save_to_file(data)

    for a in a_href:
        query = parse_query_to_dict(a['href'])
        status_code, headers, body = get(url, query)
        data, temp = extract_html_message(body)
        save_to_file(data)

    print('保存完毕.')


if __name__ == '__main__':
    main()
