import time

from models import Model


class Blog(Model):
    """
    blog 程序的数据库类
    """
    def __init__(self, form):
        self.id = form.get('id', None)
        self.author = form.get('author', '')
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.ct = form.get('ct', None)
        if self.ct is None:
            self.ct = int(time.time())

    @classmethod
    def new(cls, form):
        """
        创建一个 blog 实例
        保存实例的数据
        返回实例
        """
        b = cls(form)
        b.save()
        return b


class BlogComment(Model):
    """
    blog 程序中每篇博客的评论
    """
    def __init__(self, form):
        self.id = form.get('id', None)
        self.author = form.get('author', '')
        self.content = form.get('content', '')
        self.blog_id = int(form.get('blog_id', -1))
        self.ct = form.get('ct', None)
        if self.ct is None:
            self.ct = int(time.time())

    @classmethod
    def new(cls, form):
        """
        创建一个 comment 实例
        保存实例的数据
        返回实例
        """
        c = cls(form)
        c.save()
        return c
