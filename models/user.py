from models import Model


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

    def validate_login(self):
        """
        验证登录的账户是否存在
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

        u = User.find_by(username=self.username)
        return u is not None and u.password == self.password

    def validate_register(self):
        """
        验证注册的数据是否符合规定
        """
        return len(self.username) > 2 and len(self.password) > 2
