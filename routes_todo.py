from utils import render_template, http_response, redirect

from models.todo import Todo


def todo_index(request):
    """
    todo 程序的主页
    """
    todos = Todo.all()
    body = render_template('todo/index.html', todos=todos)

    return http_response(body)


def todo_add(request):
    """
    接受浏览器发过来的添加 todo 请求
    添加数据并发一个 302 定向给浏览器
    浏览器就会去请求 /todo，从而回到 todo 主页
    """
    # 解析画面传送过来的数据
    form = request.form()
    # 创建并保存一个 todo
    Todo.new(form)

    return redirect('/todo')


def todo_delete(request):
    """
    删除一个 todo
    """
    todo_id = int(request.query.get('id'))
    Todo.delete(todo_id)

    return redirect('/todo')


route_dict = {
    '/todo': todo_index,
    '/todo/add': todo_add,
    '/todo/delete': todo_delete,
}
