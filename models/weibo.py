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

    @classmethod
    def new(cls, form, user_id=-1):
        """
        创建并保存一个 weibo
        返回该实例
        """
        w = cls(form, user_id)
        w.save()

        return w
