import time

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

        # 添加创建和修改时间
        self.ct = form.get('ct', None)
        self.ut = form.get('ut', None)
        if self.ct is None:
            # unix 时间戳：从 1970 年 1 月 1 日（UTC/GMT的午夜）开始所经过的秒数
            # 在大多数的 UNIX 系统中 UNIX 时间戳存储为 32 位，这样会引发 2038 年问题或 Y2038。
            self.ct = int(time.time())
            self.ut = self.ct

    def format_datetime(self, unix_time):
        """
        格式化创建日期
        格式化成 2021-03-18 08:33:04 形式
        """
        value = time.localtime(unix_time)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", value)

        return dt

    @classmethod
    def new(cls, form, user_id=-1):
        """
        创建并保存一个 todo
        返回该实例
        """
        t = cls(form, user_id)
        t.save()

        return t

    @classmethod
    def update(cls, id, form):
        """
        更新一个 todo 的内容
        """
        t = cls.find_by(id=id)
        valid_names = ['task', 'ut']

        for key in form:
            # 找出需要更新的字段
            if key in valid_names:
                setattr(t, key, form[key])

        # 更改 ut 时间
        t.ut = int(time.time())
        t.save()

        return t
