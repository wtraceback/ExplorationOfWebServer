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

    # 存在一个问题，如果是空的文件，则读取到的也是 b''
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


def route_index(request):
    """
    主页的处理函数, 返回主页的响应
    """
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n'
    body = render_template('index.html')
    r = header + body

    return r.encode('utf-8')


def route_login(request):
    """
    登录页面
    """
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n'
    if request.method == 'POST':
        username = 'test'
        password = '123456'
        form = request.form()
        if form.get('username', '') == username and form.get('password', '') == password:
            result = '登陆成功'
        else:
            result = '用户名或密码错误'
    else:
        result = ''

    body = render_template('login.html')
    body = body.replace('{{result}}', result)
    r = header + '\r\n' + body

    return r.encode('utf-8')


route_dict = {
    '/': route_index,
    '/login': route_login,
}
