import time

from utils import render_template, http_response, redirect, current_user, login_required
from models.todo import Todo


@login_required
def todo_index(request):
    """
    todo 程序的主页
    """
    # todos = Todo.all()
    u = current_user(request)
    todos = []
    if u is not None:
        todos = u.todos()

    body = render_template('todo/index.html', todos=todos)

    return http_response(body)


@login_required
def todo_add(request):
    """
    接受浏览器发过来的添加 todo 请求
    添加数据并发一个 302 定向给浏览器
    浏览器就会去请求 /todo，从而回到 todo 主页
    """
    u = current_user(request)
    user_id = u.id
    # 解析画面传送过来的数据
    form = request.form()
    # 创建并保存一个 todo
    Todo.new(form, user_id)

    return redirect('/todo')


@login_required
def todo_delete(request):
    """
    删除一个 todo
    """
    todo_id = int(request.query.get('id'))
    Todo.delete(todo_id)

    return redirect('/todo')


@login_required
def todo_edit(request):
    """
    进入 todo 画面
    更新一个 todo
    """
    todo_id = int(request.query.get('id', -1))
    todo = Todo.find_by(id=todo_id)

    if request.method == 'POST':
        # 更新
        # 把 post 请求的 body 解析为一个字典
        form = request.form()
        todo.task = form.get('task')
        todo.ut = int(time.time())
        todo.save()

        return redirect('/todo')

    body = render_template('todo/edit.html', todo=todo)

    return http_response(body)


route_dict = {
    '/todo': todo_index,
    '/todo/add': todo_add,
    '/todo/delete': todo_delete,
    '/todo/edit': todo_edit,
}
