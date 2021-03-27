/*
    每一条显示 todo 的模板
 */
var todoTemplate = function(todo) {
    var task = todo.task
    var ut = dateFormat(todo.ut)

    var t = `
        <div class="todo-cell">
            <button class="todo-edit">编辑</button>
            <button class="todo-delete">删除</button>
            <span class="todo-task">${task}</span>
            <time class="todo-ut">${ut}</time>
        </div>
    `

    return t
}

/*
    往页面中插入 todo-cell
 */
var insertTodo = function(todo) {
    var cell = todoTemplate(todo)

    // 将 cell 插入到 todo-list 中
    var todo_list = $('.todo-list')
    todo_list.insertAdjacentHTML('beforeend', cell)
}

/*
    获取所有的 todo
 */
var apiTodoAll = function(callback) {
    var path = '/api/todo/all'
    ajax('GET', path, '', callback)
}

/*
    加载所有的 todo
 */
var loadTodos = function() {
    // 调用 ajax api 来加载数据
    apiTodoAll(function(r) {
        // 将服务器传送过来的 json 格式字符串转换成 对象 或 数组
        var todos = JSON.parse(r)

        // 循环添加到页面中
        for (var i = 0; i < todos.length; i++) {
            var todo = todos[i]
            insertTodo(todo)
        }
    })
}

var __main = function() {
    loadTodos()
}

__main()
