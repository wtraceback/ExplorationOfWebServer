from models.user import User
from utils import random_str, session, current_user, response_with_headers, \
                    redirect, login_required


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


def template(filename):
    path = 'templates/' + filename
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


@login_required
def index(request):
    """
    主页的处理函数, 返回主页的响应
    """
    header = response_with_headers()
    body = template('index.html')
    username = current_user(request)
    body = body.replace('{{username}}', username)
    r = header + '\r\n' + body

    return r.encode('utf-8')


def login(request):
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
    body = template('login.html')
    body = body.replace('{{result}}', result)
    body = body.replace('{{username}}', username)
    r = header + '\r\n' + body

    return r.encode('utf-8')


def register(request):
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
    body = template('register.html')
    body = body.replace('{{result}}', result)

    r = header + '\r\n' + body

    return r.encode('utf-8')


route_dict = {
    '/': index,
    '/login': login,
    '/register': register,
}
