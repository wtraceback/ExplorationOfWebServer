from models import Model


class Todo(Model):
    """
    Todo 相关的数据
    """
    def __init__(self, form, user_id=-1):
        self.id = form.get('id', None)
        self.task = form.get('task', '')
        # 和用户的 id 相关联，表明拥有它的 user 实例
        self.user_id = form.get('user_id', user_id)

    @classmethod
    def new(cls, form, user_id=-1):
        """
        创建并保存一个 todo
        返回该实例
        """
        t = cls(form, user_id)
        t.save()

        return t
