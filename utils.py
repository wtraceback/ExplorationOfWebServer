import random
import time

from models.user import User


def log(*args, **kwargs):
    """
    把 log 记录写进文件中
    """
    # 使用 Python 的 time 模块来格式化日期和时间
    # 使用 time 模块的 strftime 方法来格式化日期；time.strftime(format[, t])
    # 格式化成 2021-03-18 08:33:04 形式
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open('logs/demo.log', 'a', encoding='utf-8') as f:
        # print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)
        print(dt, *args, file=f, **kwargs)


# session 在服务器端实现过期功能
session = {
    # 'sessionid': {
    #     'username': 'test',
    #     'expired': '2021-03-14 16:07:08',
    # }
}


def login_required(route_func):
    """
    验证登录权限的装饰器
    """
    def func(request):
        username = current_user(request)
        u = User.find_by(username=username)

        if u is None:
            return redirect('/login')

        return route_func(request)

    return func


def redirect(url, headers=None):
    """
    重定向函数
    浏览器在收到 302 响应时，在 HTTP header 里面找 Location 字段并获取一个 url，然后自动请求新的 url
    HTTP/1.1 302 xxx
    Location: /

    """
    h = {
        'Location': url,
    }

    if headers is not None:
        h.update(headers)

    # 增加 Location 字段并生成 HTTP 响应返回，302 响应没有 HTTP body 部分
    r = response_with_headers(h, code=302) + '\r\n'

    return r.encode('utf-8')


def current_user(request):
    """
    返回当前访问者的用户名
    """
    session_id = request.cookies.get('user', '')
    username = session.get(session_id, '【游客】')

    return username


def response_with_headers(headers=None, code=200):
    """
    response 的响应头
    """
    code_description = {
        '200': 'OK',
        '301': 'Moved Permanently',
        '302': 'Found',
        '400': 'Bad Request',
        '401': 'Unauthorized',
        '403': 'Forbidden',
        '404': 'Not Found',
        '500': 'Internal Server Error',
    }

    h = {
        'Content-Type': 'text/html; charset=UTF-8',
    }

    if headers is not None:
        h.update(headers)

    str_code = str(code)
    header = 'HTTP/1.1 {} {}\r\n'.format(str_code, code_description.get(str_code, 'OK'))

    headers_list = ['{}: {}\r\n'.format(k, v) for k, v in h.items()]
    header += ''.join(headers_list)

    return header


def random_str():
    """
    用于生成一个随机的字符串，当做 sessionid
    """
    seed = 'abcdefghijklmnopqrstuvwxyz1234567890'
    r = []
    for i in range(16):
        # random.randint(a, b) 返回随机整数 N 满足 a <= N <= b
        random_index = random.randint(0, len(seed) - 1)
        r.append(seed[random_index])

    return ''.join(r)
