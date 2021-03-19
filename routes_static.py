from utils import response_with_headers


def template(filename):
    path = 'templates/' + filename
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


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


def static(request):
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
        # header = b'HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/html; charset=UTF-8\r\n'
        header = response_with_headers(code=404)
    else:
        suffix = filename.split('.')[-1]
        content_type = dict_suffix.get(suffix, 'text/html')
        headers = {
            'Content-Type': content_type
        }
        header = response_with_headers(headers)

    r = header.encode('utf-8') + b'\r\n' + body

    return r


route_dict = {
    '/static': static,
}
