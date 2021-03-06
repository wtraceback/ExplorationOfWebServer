import json
"""
json 是一种时下非常流行的数据格式
在 Python 中可以方便地使用 json 格式序列化/反序列化字典或者列表

json 在 Python 是一个序列化/反序列化 list/dict 的库
"""


def save(data, path):
    """
    用于保存数据
    data 为 list 数据，path 为文件的
    """
    # ensure_ascii=False 用于保存中文
    # 将 Python 对象编码成 JSON 字符串
    s = json.dumps(data, indent=4, ensure_ascii=False)

    with open(path, 'w+', encoding='utf-8') as f:
        # json.dump(data, f, indent=4, ensure_ascii=False)
        f.write(s)


def load(path):
    """
    用于从 path 中加载数据
    """
    with open(path, 'r', encoding='utf-8') as f:
        # return json.load(f)
        s = f.read()
        # 将已编码的 JSON 字符串解码为 Python 对象
        return json.loads(s)


class Model(object):
    """
    Model 是一个用于存储数据的基类
    """
    # 类方法的调用方式是  类名.类方法()
    @classmethod
    def db_path(cls):
        """
        获取调用类的类名，然后返回对应的类存储数据的路径
        """
        classname = cls.__name__
        path = '{}.json'.format(classname)

        return path

    @classmethod
    def new(cls, form):
        """
        相当于创建一个实例，如：User(form)
        """
        m = cls(form)

        return m

    @classmethod
    def all(cls):
        """
        得到一个类的所有存储的实例
        """
        path = cls.db_path()
        models = load(path)
        ms = [cls.new(m) for m in models]

        return ms

    def save(self):
        """
        save 函数用于把一个 Model 的实例保存到文件中
        """
        models = self.all()
        models.append(self)

        # __dict__ 是包含了对象所有属性和值的字典
        data = [m.__dict__ for m in models]

        path = self.db_path()
        save(data, path)

    def __repr__(self):
        """
        用于打印实例的数据
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)

        return '< {}\n{} >\n'.format(classname, s)


class User(Model):
    """
    用户账户类
    """
    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def validate_login(self):
        """
        验证登录的账户是否存在
        """
        models = self.all()
        # __dict__ 是包含了对象所有属性和值的字典
        user_list = [m.__dict__ for m in models]
        # user_list = [{'username': 'admin', 'password': '123456'}, {'username': 'test', 'password': '123456'}]

        for a in user_list:
            if a.get('username', False) == self.username and a.get('password', False) == self.password:
                return True

        return False

    def validate_register(self):
        """
        验证注册的数据是否符合规定
        """
        return len(self.username) > 2 and len(self.password) > 2
