from utils import current_user, render_template, http_response, redirect
from models.user import User


def admin_users(request):
    """
    管理员权限：查看所有的用户信息
    如果非管理员访问，则重定向到 /login 画面
    """
    u = current_user(request)
    if u is not None and u.is_admin():
        users = User.all()
        body = render_template('admin/index.html', u=u, users=users)

        return http_response(body)
    else:
        return redirect('/login')


def update_password(request):
    """
    管理员修改任意用户的密码
    """
    form = request.form()
    user_id = int(form.get('id', -1))
    new_password = form.get('password', '')

    # 根据 id 寻找对应的用户
    u = User.find_by(id=user_id)
    result = ''

    if u is not None:
        u.password = u.salt_hashed_password(new_password)
        u.save()
        result = '密码更新成功'

    return redirect('/admin/users')


route_dict = {
    '/admin/users': admin_users,
    '/admin/user/update_password': update_password,
}
