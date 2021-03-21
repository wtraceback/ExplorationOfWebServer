from utils import render_template, http_response, current_user, redirect
from models.weibo import Weibo


def weibo_index(request):
    """
    微博程序的主页
    """
    # 获取所有的 weibo
    weibos = Weibo.all()
    body = render_template('weibo/index.html', weibos=weibos)

    return http_response(body)


def weibo_personal_index(request):
    """
    个人主页
    """
    u = current_user(request)
    # 获取个人所有的 weibo
    weibos = u.weibos()

    body = render_template('weibo/personal_index.html', weibos=weibos)

    return http_response(body)


def weibo_add(request):
    """
    接受浏览器发过来的添加 weibo 请求
    添加数据并发一个 302 定向给浏览器
    浏览器就会去请求 /weibo/personal_index，从而回到 weibo 个人主页
    """
    u = current_user(request)
    if u is not None:
        # 解析页面传送过来的数据
        form = request.form()
        user_id = u.id
        # 创建并保存一个 weibo
        Weibo.new(form, user_id)

        return redirect('/weibo/personal_index')
    else:
        return redirect('/weibo/index')


def weibo_delete(request):
    """
    删除一个 weibo
    """
    weibo_id = int(request.query.get('id'))
    Weibo.delete(weibo_id)

    return redirect('/weibo/personal_index')


def weibo_edit(request):
    """
    进入 weibo 画面
    更新一个 weibo
    """
    weibo_id = int(request.query.get('id', -1))
    weibo = Weibo.find_by(id=weibo_id)

    if request.method == 'POST':
        # 更新
        # 把 post 请求的 body 解析为一个字典
        form = request.form()
        weibo.content = form.get('content')
        weibo.save()

        return redirect('/weibo/personal_index')

    body = render_template('weibo/edit.html', weibo=weibo)

    return http_response(body)


route_dict = {
    '/weibo/index': weibo_index,
    '/weibo/personal_index': weibo_personal_index,
    '/weibo/add': weibo_add,
    '/weibo/delete': weibo_delete,
    '/weibo/edit': weibo_edit,
}
