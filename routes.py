import random

from models.user import User


# session 在服务器端实现过期功能
session = {
    # 'sessionid': {
    #     'username': 'test',
    #     'expired': '2021-03-14 16:07:08',
    # }
}


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


def render_static_file(filename):
    path = 'static/' + filename
    img_suffix = ['bmp', 'jpg', 'jpeg', 'png', 'gif']
    body = b''
    is_error = False

    try:
        # 读取静态文件，如果不存在，则不存在 body
        suffix = filename.split('.')[-1]
        if suffix in img_suffix:
            # rb 表示以二进制的方式读取文件数据，图片数据需要以二进制格式打开，使用 rb
            with open(path, 'rb') as f:
                body = f.read()
        else:
            with open(path, 'r', encoding='utf-8') as f:
                body = f.read()
                body = body.encode('utf-8')
    except Exception as e:
        is_error = True

    return body, is_error


def route_static(request):
    """
    静态资源的处理函数
    """
    # content-type 的种类
    dict_suffix = {
        'html': 'text/html',
        'js': 'application/javascript',
        'css': 'text/css',
        'bmp': 'image/bmp',
        'jpg': 'image/jpg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif'
    }

    filename = request.query.get('file', '')
    body, is_error = render_static_file(filename)

    # 判断是否能读取到静态文件，根据情况来返回对应的 http 响应
    if is_error:
        header = b'HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/html; charset=UTF-8\r\n'
    else:
        suffix = filename.split('.')[-1]
        content_type = dict_suffix.get(suffix, 'text/html')

        header = 'HTTP/1.1 200 OK\r\nContent-Type: {}\r\n'.format(content_type)
        header = header.encode('utf-8')

    r = header + b'\r\n' + body

    return r


def render_template(filename):
    path = 'templates/' + filename
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


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


@login_required
def route_index(request):
    """
    主页的处理函数, 返回主页的响应
    """
    header = response_with_headers()
    body = render_template('index.html')
    username = current_user(request)
    body = body.replace('{{username}}', username)
    r = header + '\r\n' + body

    return r.encode('utf-8')


def route_login(request):
    """
    登录处理
    """
    username = current_user(request)
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_login():
            # 设置一个随机字符串当做 token 来使用
            session_id = random_str()
            session[session_id] = u.username
            headers = {}
            headers['Set-Cookie'] = 'user={}'.format(session_id)

            return redirect('/', headers=headers)
        else:
            result = '用户名或密码错误'
    else:
        result = ''

    header = response_with_headers()
    body = render_template('login.html')
    body = body.replace('{{result}}', result)
    body = body.replace('{{username}}', username)
    r = header + '\r\n' + body

    return r.encode('utf-8')


def route_register(request):
    """
    注册处理
    """
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_register():
            u.save()
            result = '注册成功'
        else:
            result = '用户名或者密码长度必须大于2'
    else:
        result = ''

    header = response_with_headers()
    body = render_template('register.html')
    body = body.replace('{{result}}', result)

    r = header + '\r\n' + body

    return r.encode('utf-8')


route_dict = {
    '/': route_index,
    '/login': route_login,
    '/register': route_register,
}
