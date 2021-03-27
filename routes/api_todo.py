import json

from models.todo import Todo
from utils import (
    json_response,
)


def all(request):
    """
    返回所有的 todo
    """
    todo_list = Todo.all()
    todos = [t.object_to_dict() for t in todo_list]

    return json_response(todos)


def add(request):
    """
    接收浏览器发送过来的 post 请求，并解析成 dict 或 list
    添加新的 todo
    将添加的 todo 的数据返回给浏览器
    """
    form = request.json()
    t = Todo.new(form)

    return json_response(t.object_to_dict())


def delete(request):
    """
    删除一个 todo
    /api/todo/delete?id=1
    """
    todo_id = int(request.query.get('id', -1))
    t = Todo.delete(todo_id)

    if t is None:
        # 返回一个空的 dict
        return json_response()
    else:
        return json_response(t.object_to_dict())


def update(request):
    """
    更新 todo
    跟 delete 的 todo id 在 url 中的不同之处
    update 的 todo id 在 request 的 body 中
    """
    form = request.json()
    todo_id = int(form.get('id'))
    t = Todo.update(todo_id, form)

    return json_response(t.object_to_dict())


# api 文件只返回 json 格式的数据
# 而不是 html 格式的数据
route_dict = {
    '/api/todo/all': all,
    '/api/todo/add': add,
    '/api/todo/delete': delete,
    '/api/todo/update': update,
}
