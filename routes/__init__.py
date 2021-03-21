from utils import current_user, login_required, render_template, http_response


@login_required
def index(request):
    """
    主页的处理函数, 返回主页的响应
    """
    u = current_user(request)
    body = render_template('index.html', user=u)

    return http_response(body)


route_dict = {
    '/': index,
}
