import json
import time
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
        path = 'db/{}.json'.format(classname)

        return path

    @classmethod
    def all(cls):
        """
        得到一个类的所有存储的实例
        """
        path = cls.db_path()
        models = load(path)
        ms = [cls(m) for m in models]

        return ms

    @classmethod
    def find_by(cls, **kwargs):
        """
        根据参数，返回一个 User 实例
        如果查找到有多条这样的数据, 返回第一个
        如果没这样的数据, 返回 None
        """
        key, value = '', ''
        # 获取传入参数的最后一个，因为字典是乱序的，所以无法确定最后一个是哪个
        for k, v in kwargs.items():
            key, value = k, v

        models = cls.all()
        # 根据传入的参数查找 models 中对应的实例
        for i in models:
            # getattr(i, key) 等价于 i.__dict__[k]，不过如果不存在这个属性值，那么将会抛出错误
            # getattr() 函数用于返回一个对象属性值
            if i.__dict__.get(key, False) == value:
                return i

        return None

    @classmethod
    def find_all(cls, **kwargs):
        """
        根据参数，以 list 的形式返回所有符合参数的值的 User 实例
        如果没这样的数据, 返回 []
        """
        key, value = '', ''
        # 获取传入参数的最后一个，因为字典是乱序的，所以无法确定最后一个是哪个
        for k, v in kwargs.items():
            key, value = k, v

        r = []
        models = cls.all()
        # 根据传入的参数查找 models 中对应的实例
        for i in models:
            # getattr(i, key) 等价于 i.__dict__[k]，不过如果不存在这个属性值，那么将会抛出错误
            # getattr() 函数用于返回一个对象属性值
            if i.__dict__.get(key, False) == value:
                r.append(i)

        return r

    @classmethod
    def delete(cls, id):
        """
        根据 id 来删除对应的数据
        """
        models = cls.all()
        index = -1
        for i, m in enumerate(models):
            if m.id == id:
                index = i
                break

        if index == -1:
            return None
        else:
            obj = models.pop(index)
            data = [m.__dict__ for m in models]
            path = cls.db_path()
            save(data, path)

            # 返回被删除的元素
            return obj

    def save(self):
        """
        save 函数用于把一个 Model 的实例保存到文件中
        """
        models = self.all()

        if self.__dict__.get('id') is None:
            # 注册用户的时候
            if len(models) > 0:
                # 在已存在的数据中找到最大的 id，并在其基础上加 1
                # id 为整数
                self.id = models[-1].id + 1
            else:
                # 第一条数据的 id 默认为 1
                self.id = 1

            models.append(self)
        else:
            # 更改已存在的用户信息
            # 在更新用户信息画面，后端给前端传递了对应的 user id，前端请求时又传回来并设置了 request 对象的 id
            # enumerate 枚举    获取下标以及元素本身
            for i, m in enumerate(models):
                if m.id == self.id:
                    models[i] = self
                    break

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

    def object_to_dict(self):
        """
        返回当前 model 的字典表示
        """
        # Python 字典 copy() 函数返回一个字典的浅复制。
        # dict.copy()
        # 浅拷贝：深拷贝父对象（一级目录），子对象（二级目录）不拷贝，子对象是引用
        d = self.__dict__.copy()
        return d

    def format_datetime(self, unix_time):
        """
        格式化创建日期
        格式化成 2021-03-18 08:33:04 形式
        """
        value = time.localtime(unix_time)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", value)

        return dt
