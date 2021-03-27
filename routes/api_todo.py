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


# api 文件只返回 json 格式的数据
# 而不是 html 格式的数据
route_dict = {
    '/api/todo/all': all,
}
