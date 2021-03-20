from models import Model
from models.todo import Todo


class User(Model):
    """
    用户账户类
    """
    def __init__(self, form):
        self.id = form.get('id', None)
        if self.id is not None:
            self.id = int(self.id)
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.role = int(form.get('role', 10))

    def validate_login(self):
        """
        验证登录的账户是否存在
        验证登录的密码是否正确
        """
        # models = self.all()
        # # __dict__ 是包含了对象所有属性和值的字典
        # user_list = [m.__dict__ for m in models]
        # # user_list = [{'username': 'admin', 'password': '123456'}, {'username': 'test', 'password': '123456'}]
        #
        # for a in user_list:
        #     if a.get('username', False) == self.username and a.get('password', False) == self.password:
        #         return True
        #
        # return False
        # 查找数据库中存在的用户
        u = User.find_by(username=self.username)

        if u is not None:
            pwd = self.salt_hashed_password(self.password)
            # 判断数据库中的密码 u.password 是否和登录输入的密码哈希值一样
            return u.password == pwd
        else:
            return False

    def validate_register(self):
        """
        验证注册的数据是否符合规定
        """
        return len(self.username) > 2 and len(self.password) > 2

    def add_user(self):
        """
        为了避免和类方法 all() 中生成的实例相冲突（重复使用 md5 生成哈希密码）
        重新定义一个函数用来生成用户
        """
        pwd = self.password
        self.password = self.salt_hashed_password(pwd)
        if User.find_by(username=self.username) is None:
            self.save()
            return self
        else:
            return None

    def is_admin(self):
        """
        判断当前的登录用户是否是管理员权限
        1 为管理员权限
        """
        return self.role == 1

    def todos(self):
        """
        数据关联 一对多的关系
        """
        # return [t for t in Todo.all() if t.user_id == self.id]
        ts = []
        for t in Todo.all():
            if t.user_id == self.id:
                ts.append(t)

        return ts

    def hashed_password(self, password):
        """
        使用 md5 生成哈希密码
        """
        import hashlib

        # 用 ascii 编码转换成 bytes 对象
        p = password.encode('ascii')
        s = hashlib.sha256(p)

        # 返回摘要字符串
        return s.hexdigest()

    def salt_hashed_password(self, password, salt='abc[];,./123'):
        """
        生成一个带盐的密文
        一个 md5 + salt 的哈希密码
        """
        import hashlib
        def sha256(s):
            # 用 ascii 编码转换成 bytes 对象
            ascii_str = s.encode('ascii')
            return  hashlib.sha256(ascii_str).hexdigest()

        h1 = sha256(password)
        # 使用 哈希的密码 + salt
        h2 = sha256(h1 + salt)

        # 返回摘要字符串
        return h2
