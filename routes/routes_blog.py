from models.blog import (
    Blog,
    BlogComment,
)
from utils import (
    render_template,
    http_response,
    redirect,
)


def index(request):
    """
    blog 的主页，显示个人的博客清单
    """
    blogs = Blog.all()
    body = render_template('blog/index.html', blogs=blogs)
    return http_response(body)


def new(request):
    """
    新建博文画面
    """
    body = render_template('blog/new.html')
    return http_response(body)


def add(request):
    """
    保存新的博文
    """
    form = request.form()
    b = Blog.new(form)
    return redirect('/blog/index')


def post(request):
    """
    根据 id 显示博文
    """
    blog_id = int(request.query.get('id', -1))
    blog = Blog.find_by(id=blog_id)
    comments = BlogComment.find_all(blog_id=blog_id)
    body = render_template('blog/post.html', blog=blog, comments=comments)
    return http_response(body)


def comment(request):
    """
    添加新的评论
    """
    form = request.form()
    BlogComment.new(form)
    return redirect('/blog/post?id=' + str(form.get('blog_id')))


route_dict = {
    '/blog/index': index,
    '/blog/new': new,
    '/blog/add': add,
    '/blog/post': post,
    '/blog/comment/new': comment,
}
