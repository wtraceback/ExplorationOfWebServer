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

/*
    edit 输入框的模板
*/
var insertEditForm = function(cell) {
    // 由于每一条 todo 都会有这个编辑框，因此不能添加 id 属性
    var form = `
        <div class='todo-edit-form'>
            <input type="text" class="todo-edit-input">
            <button class="todo-update">更新</button>
        </div>
    `

    cell.insertAdjacentHTML('beforeend', form)
}

/*
    编辑 todo
*/
var bindEventTodoEdit = function() {
    var todo_list = $('.todo-list')
    todo_list.addEventListener('click', function(event) {
        var self = event.target
        if (self.classList.contains('todo-edit')) {
            // 编辑这个 todo，在元素的下方添加输入框和 update 按钮
            var cell = self.parentElement

            // 添加 if 判断，用于判断是否已经存在了更新标签，防止重复添加
            if (cell.querySelector('.todo-edit-form') == null) {
                insertEditForm(cell)
            }
        }
    })
}

var apiTodoUpdate = function(form, callback) {
    var path = '/api/todo/update'
    ajax('POST', path, form, callback)
}

/*
    更新 todo
*/
var bindEventTodoUpdate = function() {
    var todo_list = $('.todo-list')
    todo_list.addEventListener('click', function(event) {
        var self = event.target
        if (self.classList.contains('todo-update')) {
            // 获取对应 todo 中的 input 的值
            var edit_form = self.parentElement
            var input = edit_form.querySelector('.todo-edit-input')
            var task = input.value
            // 通过 closest 方法找到最近的直系父节点，获取当前 todo 的 id
            var cell = self.closest('.todo-cell')
            var todo_id = cell.dataset.id
            var form = {
                'id': todo_id,
                'task': task,
            }

            apiTodoUpdate(form, function(r) {
                var todo = JSON.parse(r)
                // var selector = '#todo-' + todo.id
                // var cell = $(selector)
                // 上面的 cell 变量依然还可以在匿名函数中使用
                var task_content = cell.querySelector('.todo-task')
                var ut_content = cell.querySelector('.todo-ut')
                task_content.innerHTML = todo.task
                ut_content.innerHTML = dateFormat(todo.ut)

                // 更新成功后，清除 edit-form
                edit_form.remove()

                // 方法二，将一整个 todo-cell 标签替换掉
            })
        }
    })
}

var bindEvents = function() {
    bindEventTodoAdd()
    bindEventTodoDelete()
    bindEventTodoEdit()
    bindEventTodoUpdate()
}

var __main = function() {
    bindEvents()
    loadTodos()
}

__main()
