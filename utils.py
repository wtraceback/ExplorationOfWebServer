import random
import time
from jinja2 import FileSystemLoader, Environment
import os.path
import json

from models.user import User
from routes.session import session


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


def login_required(route_func):
    """
    验证登录权限的装饰器
    """
    def func(request):
        u = current_user(request)

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
    user_id = int(session.get(session_id, '-1'))
    u = User.find_by(id=user_id)

    return u


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


def http_response(body, headers=None, code=200):
    """
    返回 response 相关的信息
    """
    header = response_with_headers(headers, code)
    r = header + '\r\n' + body

    return r.encode('utf-8')


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


# __file__ 是当前文件的名字
# 获取当前文件所在的路径，用于得到加载模板的目录
path = '{}/templates/'.format(os.path.dirname(__file__))
# 创建一个加载器, jinja2 会从这个目录中加载模板
loader = FileSystemLoader(path)
# 用加载器创建一个环境, 有了它才能读取模板文件
env = Environment(loader=loader)


def render_template(path, **kwargs):
    """
    本函数接受一个路径和一系列参数
    加载模板
    渲染
    返回渲染后的 html 字符串
    调用：render_template('demo.html', name='Test', result='测试结果')
    """
    # template = env.get_template('demo.html')
    # name='Test'
    # r = template.render(name=name, result='测试结果')

    template = env.get_template(path)       # 调用 get_template() 方法加载模板
    r = template.render(**kwargs)           # 调用 render() 方法渲染模板

    return r


def error(request, code=404):
    """
    根据 code 返回不同的错误响应
    """
    e = {
        404: b'HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n<h1>NOT FOUND</h1>',
    }

    return e.get(code, b'')


def json_response(data={}):
    """
    json 格式的 body 数据
    返回 response 响应
    """
    headers = {
        'Content-Type': 'application/json'
    }

    header = response_with_headers(headers)
    # json.dumps 用于把 list 或者 dict 转化为 json 格式的字符串
    # indent=4 表示格式化缩进, 方便好看用的
    # ensure_ascii=False 可以正确处理中文
    body = json.dumps(data, indent=4, ensure_ascii=False)
    r = header + '\r\n' + body

    return r.encode('utf-8')
