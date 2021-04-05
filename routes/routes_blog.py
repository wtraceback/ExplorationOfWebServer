from utils import (
    render_template,
    http_response,
)


def index(request):
    """
    blog 的主页，显示个人的博客清单
    """
    body = render_template('blog/index.html')
    return http_response(body)


route_dict = {
    '/blog/index': index,
}
