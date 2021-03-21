from models import Model


class Comment(Model):
    """
    评论相关的数据库类
    """
    def __init__(self, form, user_id=-1):
        self.id = form.get('id', None)
        self.content = form.get('content', '')

        # 和用户的 id 相关联，用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', user_id)
        self.weibo_id = int(form.get('weibo_id', -1))

    def user(self):
        """
        根据 user_id 找到当前的用户
        返回一个 User 的实例
        """
        from models.user import User
        u = User.find_by(id=self.user_id)

        return u
