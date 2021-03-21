from models import Model


class Weibo(Model):
    """
    微博程序的数据库类
    """
    def __init__(self, form, user_id=-1):
        self.id = form.get('id', None)
        self.content = form.get('content', '')
        # 和用户的 id 相关联，表明拥有它的 user 实例
        self.user_id = form.get('user_id', user_id)

    def user(self):
        """
        根据 user_id 找到当前的用户
        返回一个 User 的实例
        """
        from models.user import User
        u = User.find_by(id=self.user_id)

        return u

    def comments(self):
        """
        当前 weibo 的所有评论
        """
        # return [c for c in Comment.all() if c.weibo_id == self.id]
        from models.comment import Comment
        return Comment.find_all(weibo_id=self.id)

    @classmethod
    def new(cls, form, user_id=-1):
        """
        创建并保存一个 weibo
        返回该实例
        """
        w = cls(form, user_id)
        w.save()

        return w
