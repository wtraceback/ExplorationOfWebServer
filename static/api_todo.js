/*
    每一条显示 todo 的模板
*/
var todoTemplate = function(todo) {
    var id = todo.id
    var task = todo.task
    var ut = dateFormat(todo.ut)

    var t = `
        <div class="todo-cell" data-id="${id}">
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

/*
    添加新的 todo
*/
var apiTodoAdd = function(form, callback) {
    var path = '/api/todo/add'
    ajax('POST', path, form, callback)
}

/*
    绑定 todo add 按钮
*/
var bindEventTodoAdd = function() {
    var add_butn = $('#id-butn-add')

    // 为 add 按钮绑定 click 事件
    add_butn.addEventListener('click', function() {
        var input = $('#id-input-todo')
        var task = input.value
        var form = {
            'task': task,
        }

        apiTodoAdd(form, function(r) {
            // 收到服务器返回的数据，插入到页面中
            var todo = JSON.parse(r)
            insertTodo(todo)
            // 清空输入框的值
            input.value = ''
        })
    })
}

var apiTodoDelete = function(id, callback) {
    var path = '/api/todo/delete?id=' + id
    ajax('GET', path, '', callback)
}

/*
    通过事件委托，绑定 todo delete 按钮
*/
var bindEventTodoDelete = function() {
    var todo_list = $('.todo-list')
    todo_list.addEventListener('click', function(event) {
        var self = event.target
        if (self.classList.contains('todo-delete')) {
            // 删除这个 todo
            var cell = self.parentElement
            var todo_id = cell.dataset.id
            apiTodoDelete(todo_id, function(r) {
                log('删除成功')
                cell.remove()
            })
        }
    })
}

var bindEvents = function() {
    bindEventTodoAdd()
    bindEventTodoDelete()
}

var __main = function() {
    bindEvents()
    loadTodos()
}

__main()
