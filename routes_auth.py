from models.user import User
from utils import random_str, session, response_with_headers, \
                    redirect, login_required, render_template, http_response


def login(request):
    """
    登录处理
    """
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_login():
            user = User.find_by(username=u.username)
            # 设置一个随机字符串当做 token 来使用
            # 设置 session
            session_id = random_str()
            session[session_id] = user.id
            headers = {}
            headers['Set-Cookie'] = 'user={}'.format(session_id)

            return redirect('/', headers=headers)
        else:
            result = '用户名或密码错误'
    else:
        result = ''

    body = render_template('login.html', result=result)

    return http_response(body)


def register(request):
    """
    注册处理
    """
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_register():
            u.save()
            result = '注册成功'
            return redirect('/login')
        else:
            result = '用户名或者密码长度必须大于2'
    else:
        result = ''

    body = render_template('register.html', result=result)

    return http_response(body)


route_dict = {
    '/login': login,
    '/register': register,
}
