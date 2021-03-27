from utils import (
    render_template,
    http_response,
)


def index(request):
    """
    api todo 程序的主页的处理函数，返回主页的响应
    """
    body = render_template('api_todo/index.html')
    return http_response(body)


route_dict = {
    '/api/todo/index': index,
}
